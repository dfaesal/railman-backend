from rest_framework import generics, status
from core_app.serializers import CustomerSerializer, CitySerializer, OrderSerializer, RestaurantSerializer, MenuItemSerializer
from .models import City, Customer, Order, Restaurant, PnrDetail, MenuItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class RestaurantListByPNR(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        pnr = self.request.query_params.get('pnr')
        location = self.request.query_params.get('location')
        try:
            if location:
                restaurants = Restaurant.objects.filter(city__name=location)
            else:
                pnrDetails = PnrDetail.objects.get(pnr=pnr)
                restaurants = Restaurant.objects.filter(city__name__in=[pnrDetails.start_location, pnrDetails.end_location])
        except:
            restaurants = Restaurant.objects.none()
        return restaurants

class Orders(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        restaurant_name = data.get('restaurant')
        try:
            restaurant = Restaurant.objects.get(name=restaurant_name)
        except Restaurant.DoesNotExist:
            raise ValidationError(f"Restaurant '{restaurant_name}' does not exist")
        data['restaurant'] = restaurant.id
        item_names = data.get('orderItems')
        data['items'] = []
        for item_name in item_names:
            try:
                item = MenuItem.objects.get(name=item_name)
            except MenuItem.DoesNotExist:
                raise ValidationError(f"Menu item '{item_name}' does not exist")
            data['items'].append(item.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant = self.kwargs.get('restaurant')
        user_id = self.kwargs.get('user_id')
        pk = self.kwargs.get('pk')
        try:
            if user_id:
                queryset = Order.objects.filter(user_id=user_id, id=pk)
            else:
                queryset = Order.objects.filter(restaurant__name=restaurant, id=pk)
        except:
            queryset = Order.objects.none()
        return queryset

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        name = self.kwargs.get('restaurant')
        user = self.kwargs.get('user_id', None)
        try:
            if user:
                queryset = Order.objects.filter(user_id=user)
            else:    
                restaurant = Restaurant.objects.get(name=name)
                queryset = Order.objects.filter(restaurant=restaurant)
        except:
            queryset = Order.objects.none()
        return queryset

class MenuItemsList(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    def get_queryset(self):
        name = self.kwargs.get('restaurant')
        try:
            restaurant = Restaurant.objects.get(name=name)
            queryset = MenuItem.objects.filter(restaurant=restaurant)
        except:
            queryset = MenuItem.objects.none()
        return queryset

