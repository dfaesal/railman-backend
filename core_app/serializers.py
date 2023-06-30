from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, City, Order, Restaurant, MenuItem

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'restaurant']
        
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Customer
        fields = ['id', 'user', 'name', 'phone', 'email', 'address', 'pincode', 'password', 'role', 'city']

class OrderSerializer(serializers.ModelSerializer):
    customerName = serializers.SerializerMethodField()
    orderItems = serializers.SerializerMethodField()
    restaurantName = serializers.CharField(source='restaurant.__str__', read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'restaurant', 'items','orderItems', 'total_cost', 'timestamp', 'status', 'customerName', 'restaurantName')

    def get_customerName(self, obj):
        return obj.user.username

    def get_orderItems(self, obj):
        items_names = obj.items.values_list('name', flat=True)
        return list(items_names)

class RestaurantSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.__str__', read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'user', 'name', 'phone', 'email', 'address', 'pincode', 'password', 'city', 'role', 'rating']

 