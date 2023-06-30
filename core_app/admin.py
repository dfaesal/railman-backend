from django.contrib import admin
from .models import Customer, Restaurant, MenuItem, City, Order, Payment, PnrDetail
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(City)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(PnrDetail)