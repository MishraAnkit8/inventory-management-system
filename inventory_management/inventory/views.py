from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_access_token, generate_refresh_token
import json
from .models import User , InventoryManagement, InventoryUpdate
from .user_details import get_user_by_email
from django.core.exceptions import ValidationError
from .forms import UserRegistrationForm, InventoryManagementForm

from django.contrib.auth import authenticate, login

from .redis_cache import redis_client

from decimal import Decimal


# home page view 

def homepage_view(request):
    return render(request, 'inventory/template/homepage.html')


def register_page(request):
    return render(request, 'inventory/template/register.html')




# for user registration 

def user_registration(request):
    if request.method == 'POST':
        try:
            # Load the JSON data from the request body
            data = json.loads(request.body)

            print('data coming from frontend <<<<>>>>', data)

            register_data = data.get('registerFormData')
            print('register_data ===<<<<<>>>>', register_data)

            # Check if register_data is present
            if not register_data:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'No registration data provided.'
                }, status=400)

            # Extract user details
            email = register_data.get('userEmail')
            mobile_no = register_data.get('mobileNo')

            print(f"Checking email: {email}, mobile number: {mobile_no}")

            print('User in side view ===<<<>', User)
            if User.objects.filter(Q(email=email) | Q(mobile_no=mobile_no)).exists():
                print('yes inside if condition ')
                return JsonResponse({
                    'status': 'Done',
                    'message': 'A user with this email or mobile number is already registered.'
                }, status=200)
            

            # Populate form with extracted data
            form = UserRegistrationForm({
                'first_name': register_data.get('firstName'),
                'last_name': register_data.get('lastName'),
                'email': email,
                'mobile_no': mobile_no,
                'password': register_data.get('userPassword')
            })

            print('Form errors:', form.errors)


            # Validate form data
            if form.is_valid():
                print('insert is valid from ')
                
                # Create and save the user
                user = form.save(commit=False)
                # print('user  <<<>>>>', user)
                # user.set_password(form.cleaned_data['password'])
                user.save()
                
                

                # Respond with success
                return JsonResponse({
                    'status': 'Done',
                    'message': 'User registered successfully.'
                }, status=200)
            else:
                # Respond with form errors
                return JsonResponse({
                    'status': 'Error',
                    'errors': form.errors.as_json()  
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'Error',
                'message': 'Invalid JSON data provided.'
            }, status=400)

        except Exception as e:
            # General exception handling
            print("Error occurred:", str(e))
            return JsonResponse({
                'status': 'Error',
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=500)

    # If request method is not POST, return error
    return JsonResponse({
        'status': 'Error',
        'message': 'Invalid request method.'
    }, status=400)




def login_page_view(request): 
    return render(request, 'inventory/template/login.html')



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['loginDetails']['userEmail']
        password = data['loginDetails']['userPassword']
        
        print('data comming from template <<<<>>>>>', data)


        user = get_user_by_email(email)
        
        print('user in views  ====<<<<<>>>>>', user)
        if user:
            login(request, user)
            
            # Generate tokens
            access_token = generate_access_token(user.id)
            print('access_token ===<<<<>>>>>', access_token)
            refresh_token = generate_refresh_token(user.id)
            print('refresh_token ===<<<<>>>>', refresh_token)

            # Store tokens in Redis for session management
            redis_client.set(f"user:{user.id}:access_token", access_token, ex=3600)
            redis_client.set(f"user:{user.id}:refresh_token", refresh_token, ex=604800)

            # Set session data
            print('user id for session data ===<<<<>>>', user.id)
            request.session['user_id'] = user.id

           

            response = JsonResponse({
                'status': 'Done',
                'message': 'User logged in successfully!',
                'accessToken': access_token,
                'refreshToken': refresh_token
            })

            # Set tokens in HttpOnly cookies
            response.set_cookie('access_token', access_token, httponly=True, secure=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)

            return response

        else:
            return JsonResponse({'status': 'Error', 'message': 'Invalid email or password.'}, status=401)

    return JsonResponse({'message': 'Invalid request'}, status=400)




def render_dashbord_page(request):
    return render(request, 'inventory/template/dashboard.html')




#  from retrive inventory store data

def render_inventory_store(request):
    print('request.session.get ===<<<>>>', request.session.get('user_id'))
    if not request.session.get('user_id'): 
        return redirect('login') 


    inventory_items = InventoryManagement.objects.filter(active=True).order_by('-id')

    print('inventory_items ===<<<>>>>', inventory_items)


    context = {
        'inventory_items': inventory_items,
    } 
    
    print('context ===<<<>>>>', context)
    return render(request, 'inventory/template/inventory.html', context)







#  insert data into inventory

@csrf_exempt 
def insert_inventory_details(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        form_data = data.get('inventoryForm')

        # Prepare form data for validation and insertion
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
            
            # Return a success response to the frontend
            return JsonResponse({'status': 'Done', 'message': 'Inventory details added successfully'})
        else:
            # Return an error response with form validation errors
            return JsonResponse({'status': 'Error', 'message': form.errors}, status=400)

    return JsonResponse({'status': 'Error', 'message': 'Invalid request method'}, status=405)




# for update the inventory

@csrf_exempt
def inventory_details_update(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Data coming from frontend ===>>>', data)

            update_form = data.get('updateInventoryForm', {})
            inventory_id = update_form.get('inventoryId')
            inventory_name = update_form.get('inventoryName')
            inventory_product = update_form.get('inventoryProduct')
            invetory_platform = update_form.get('plateformName')  
            invetory_prize = update_form.get('inventoryPrize')    

            # Fetch the existing inventory item based on the ID
            inventory = get_object_or_404(InventoryUpdate, id=inventory_id)
            print('Inventory ===>>>', inventory)

            # Update the fields
            inventory.inventory_name = inventory_name
            inventory.inventory_product = inventory_product
            inventory.invetory_platform = invetory_platform  
            inventory.invetory_prize = invetory_prize      
            inventory.save()

            return JsonResponse({'status': 'Done', 'message': 'Inventory updated successfully!'})

        except InventoryUpdate.DoesNotExist:
            return JsonResponse({'status': 'Error', 'errorCode': '404', 'message': 'Inventory item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'errorCode': '500', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'Error', 'errorCode': '405', 'message': 'Method not allowed'}, status=405)
    




#  for delete row from the inventory table
@csrf_exempt
def deactivate_inventory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inventory_id = data.get('inventoryId')
            print('inventory_id ===<<<>>>', inventory_id)

            inventory = get_object_or_404(InventoryUpdate, id=inventory_id)


            inventory.active = False
            inventory.save()

            return JsonResponse({'status': 'Done', 'message': 'Inventory item deactivated successfully!'})

        except Exception as e:
            return JsonResponse({'status': 'Error', 'errorCode': '500', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'Error', 'errorCode': '405', 'message': 'Method not allowed'}, status=405)