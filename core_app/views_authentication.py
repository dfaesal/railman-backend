from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from core_app.models import Customer, City, Restaurant
from core_app.serializers import CustomerSerializer, RestaurantSerializer

####################   Authentication - register 

@api_view(['POST'])
def register(request):
	if request.method == 'POST':
		new_user_data = JSONParser().parse(request)
		user_email = new_user_data['email']
		user_role = new_user_data['role']
		if user_email is not None and user_role is not None:
			customers = Customer.objects.all()
			customer = customers.filter(email__icontains=user_email) 
			if(len(customer) == 0):
				city, created = City.objects.get_or_create(name=new_user_data.get('city'))
				new_user_data['city'] = city.id
				user, created = User.objects.get_or_create(username=new_user_data.get('name'))
				if created:
					user.set_password(new_user_data.get('password'))
					user.save()
					new_user_data['user'] = user.id
				if(user_role == "restaurant"):
					serializer = RestaurantSerializer(data=new_user_data)
					if serializer.is_valid():
						serializer.save()
				elif (user_role == "customer"):
					serializer = CustomerSerializer(data=new_user_data)
					if serializer.is_valid():
						serializer.save()
				else:
					return JsonResponse({'message': 'Role Not supported!'}, status=status.HTTP_204_NO_CONTENT)
				return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return JsonResponse({'message': 'User already exists!'}, status=status.HTTP_202_ACCEPTED)
		else:
			return JsonResponse({'message': 'Check the registration details again!'}, status=status.HTTP_204_NO_CONTENT)

####################   Authentication - login 

@api_view(['POST'])
def login(request):
	if request.method == 'POST':
		user_data = JSONParser().parse(request)
		user_email = user_data['email']
		user_password = user_data['password']
		user_role = user_data['role']
		if user_email is not None and user_role is not None and user_password is not None:
			restaurants = Restaurant.objects.all()
			restaurant = restaurants.filter(email=user_email,
									password=user_password,
									role=user_role)
			customers = Customer.objects.all()
			customer = customers.filter(email=user_email,
									password=user_password,
									role=user_role)
			if(len(customer) != 0 or len(restaurant) != 0):
				if (user_role == "customer" or user_role == "restaurant"):
					if user_role == "customer":
						serializer = CustomerSerializer(customer, many=True)
					if user_role == "restaurant":
						serializer = RestaurantSerializer(restaurant, many=True)
					return JsonResponse(serializer.data, safe=False)
				else:
					return JsonResponse({'message': 'Role Not supported!'}, status=status.HTTP_204_NO_CONTENT)       	
			else:
				return JsonResponse({'message': 'Check the login details again!'}, status=status.HTTP_204_NO_CONTENT)       
		else:
			return JsonResponse({'message': 'Check the login details again!'}, status=status.HTTP_204_NO_CONTENT)
