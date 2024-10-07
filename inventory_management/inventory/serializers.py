# inventory/serializers.py
from rest_framework import serializers
from .models import InventoryManagement

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryManagement
        fields = ['id', 'inventory_name', 'inventory_product', 'invetory_platform', 'invetory_prize']
