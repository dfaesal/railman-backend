from django.urls import path
from core_app import views
from core_app import views_authentication

urlpatterns = [
    path('api/authentication/register', views_authentication.register),
    path('api/authentication/login', views_authentication.login),
    path('api/core/cities/', views.CityList.as_view()),
    path('api/core/cities/<int:pk>/', views.CityDetail.as_view()),
    path('api/core/customers/', views.CustomerList.as_view()),
    path('api/core/customers/<int:pk>/', views.CustomerDetail.as_view()),
    path('api/core/restaurant/', views.RestaurantList.as_view()),
    path('api/core/restaurant/<int:pk>/', views.RestaurantDetail.as_view()),
    #api/core/restaurants?pnr=1234
    path('api/core/restaurants/', views.RestaurantListByPNR.as_view()),
    path('api/core/orders/', views.Orders.as_view()),
    path('api/core/orders/<int:user_id>/', views.OrderList.as_view()),
    path('api/core/orders/<str:restaurant>/', views.OrderList.as_view()),
    path('api/core/orders/<int:user_id>/<int:pk>/', views.OrderDetail.as_view()),
    path('api/core/orders/<str:restaurant>/<int:pk>/', views.OrderDetail.as_view()),
    path('api/core/<str:restaurant>/menuItems/', views.MenuItemsList.as_view()),
]