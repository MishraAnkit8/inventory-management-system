# inventory/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, InventoryManagement

class InventoryAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='ankit.mishra10021997@gmail.com',  
            password='pass@123',
            mobile_no='909882158'
        )
        self.token = self._get_jwt_token()

    def _get_jwt_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'ankit.mishra10021997@gmail.com',  
            'password': 'pass@123'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_create_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('inventory_details'), data={
            'inventory_name': 'Test Item',
            'inventory_product': 'Test Product',
            'invetory_platform': 'Test Platform',
            'invetory_prize': 100.00
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        create_response = self.client.post(reverse('inventory_details'), data={
            'inventory_name': 'Read Test Item',
            'inventory_product': 'Read Test Product',
            'invetory_platform': 'Read Test Platform',
            'invetory_prize': 50.00
        })
        item_id = create_response.data['id']
        response = self.client.get(reverse('inventory_detail', kwargs={'pk': item_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['inventory_name'], 'Read Test Item')

    def test_update_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        create_response = self.client.post(reverse('inventory_details'), data={
            'inventory_name': 'Update Test Item',
            'inventory_product': 'Update Test Product',
            'invetory_platform': 'Update Test Platform',
            'invetory_prize': 75.00
        })
        item_id = create_response.data['id']
        response = self.client.put(reverse('inventory_detail', kwargs={'pk': item_id}), data={
            'inventory_name': 'Updated Item',
            'inventory_product': 'Updated Product',
            'invetory_platform': 'Updated Platform',
            'invetory_prize': 150.00
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        create_response = self.client.post(reverse('inventory_details'), data={
            'inventory_name': 'Delete Test Item',
            'inventory_product': 'Delete Test Product',
            'invetory_platform': 'Delete Test Platform',
            'invetory_prize': 25.00
        })
        item_id = create_response.data['id']
        response = self.client.delete(reverse('inventory_detail', kwargs={'pk': item_id}))
     
