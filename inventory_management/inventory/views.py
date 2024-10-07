from venv import logger
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm, InventoryManagementForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_access_token, generate_refresh_token
import json
import logging
from .models import User, InventoryManagement, InventoryUpdate
from .user_details import get_user_by_email
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import login
from .redis_cache import redis_client
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import InventorySerializer

class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = InventoryManagement.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class InventoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryManagement.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Home page view
def homepage_view(request):
    return render(request, 'inventory/template/homepage.html')

# User registration view
def register_page(request):
    return render(request, 'inventory/template/register.html')

@csrf_exempt
def user_registration(request):
    """Handle user registration."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            register_data = data.get('registerFormData')

            if not register_data:
                return JsonResponse({'status': 'Error', 'message': 'No registration data provided.'}, status=400)

            email = register_data.get('userEmail')
            mobile_no = register_data.get('mobileNo')

            # Check for existing user
            if User.objects.filter(Q(email=email) | Q(mobile_no=mobile_no)).exists():
                return JsonResponse({'status': 'Done', 'message': 'A user with this email or mobile number is already registered.'}, status=200)

            # Populate form with extracted data
            form = UserRegistrationForm({
                'first_name': register_data.get('firstName'),
                'last_name': register_data.get('lastName'),
                'email': email,
                'mobile_no': mobile_no,
                'password': register_data.get('userPassword')
            })

            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                return JsonResponse({'status': 'Done', 'message': 'User registered successfully.'}, status=200)
            else:
                return JsonResponse({'status': 'Error', 'errors': form.errors.as_json()}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'Error', 'message': 'Invalid JSON data provided.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'Error', 'message': 'Invalid request method.'}, status=400)

def login_page_view(request): 
    return render(request, 'inventory/template/login.html')

@csrf_exempt
def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['loginDetails']['userEmail']
        password = data['loginDetails']['userPassword']

        user = get_user_by_email(email)
        if user:
            login(request, user)

            # Generate tokens
            access_token = generate_access_token(user.id)
            refresh_token = generate_refresh_token(user.id)

            # Store tokens in Redis for session management
            redis_client.set(f"user:{user.id}:access_token", access_token, ex=3600)
            redis_client.set(f"user:{user.id}:refresh_token", refresh_token, ex=604800)

            request.session['user_id'] = user.id

            response = JsonResponse({
                'status': 'Done',
                'message': 'User logged in successfully!',
                'accessToken': access_token,
                'refreshToken': refresh_token
            })
            response.set_cookie('access_token', access_token, httponly=True, secure=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)

            return response
        else:
            return JsonResponse({'status': 'Error', 'message': 'Invalid email or password.'}, status=401)

    return JsonResponse({'message': 'Invalid request'}, status=400)

def render_dashbord_page(request):
    """Render the dashboard page."""
    return render(request, 'inventory/template/dashboard.html')

def render_inventory_store(request):
    """Render the inventory store page."""
    if not request.session.get('user_id'): 
        return redirect('login') 

    inventory_items = InventoryManagement.objects.filter(active=True).order_by('-id')
    context = {'inventory_items': inventory_items}
    return render(request, 'inventory/template/inventory.html', context)

@csrf_exempt 
def insert_inventory_details(request):
    """Insert inventory details into the database."""
    if request.method == 'POST':
        data = json.loads(request.body)
        form_data = data.get('inventoryForm')

        form = InventoryManagementForm({
            'inventory_name': form_data['inventoryName'],
            'inventory_product': form_data['inventoryProduct'],
            'invetory_platform': form_data['plateformName'],
            'invetory_prize': form_data['inventoryPrize']
        })

        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = 'Admin'  
            inventory.modified_by = 'Admin'  
            inventory.save()
            return JsonResponse({'status': 'Done', 'message': 'Inventory details added successfully'})
        else:
            return JsonResponse({'status': 'Error', 'message': form.errors}, status=400)

    return JsonResponse({'status': 'Error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def inventory_details_update(request):
    """Update inventory details."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            update_form = data.get('updateInventoryForm', {})
            inventory_id = update_form.get('inventoryId')

            # Fetch existing inventory item
            inventory = get_object_or_404(InventoryUpdate, id=inventory_id)

            # Update fields
            inventory.inventory_name = update_form.get('inventoryName')
            inventory.inventory_product = update_form.get('inventoryProduct')
            inventory.invetory_platform = update_form.get('plateformName')  
            inventory.invetory_prize = update_form.get('inventoryPrize')      
            inventory.save()

            return JsonResponse({'status': 'Done', 'message': 'Inventory updated successfully!'})

        except InventoryUpdate.DoesNotExist:
            return JsonResponse({'status': 'Error', 'errorCode': '404', 'message': 'Inventory item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'errorCode': '500', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'Error', 'errorCode': '405', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def deactivate_inventory(request):
    """Deactivate an inventory item."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inventory_id = data.get('inventoryId')
            inventory = get_object_or_404(InventoryUpdate, id=inventory_id)

            inventory.active = False
            inventory.save()

            return JsonResponse({'status': 'Done', 'message': 'Inventory item deactivated successfully!'})

        except Exception as e:
            return JsonResponse({'status': 'Error', 'errorCode': '500', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'Error', 'errorCode': '405', 'message': 'Method not allowed'}, status=405)
