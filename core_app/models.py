from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=20,blank=False, default='')

class Customer(models.Model):
    def __str__(self):
        return self.name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, blank=True, default='')
    email = models.CharField(max_length=200,blank=False, default='')
    password = models.CharField(max_length=200,blank=False, default='')
    phone = models.IntegerField(blank=True)
    address = models.CharField(max_length=200,blank=True, default='')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=10, blank=True)
    pincode = models.IntegerField(blank=True)

class Restaurant(models.Model):
    def __str__(self):
        return self.name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, blank=True, default='')
    email = models.CharField(max_length=210,blank=False, default='')
    password = models.CharField(max_length=200,blank=False, default='')    
    phone = models.IntegerField(blank=True)
    address = models.CharField(max_length=200,blank=True, default='')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    pincode = models.IntegerField(blank=True)
    role = models.CharField(max_length=10, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

class MenuItem(models.Model):
    def __str__(self):
        return self.name
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

class Payment(models.Model):
    def __str__(self):
        return f'{str(self.id)}'
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment')
    payment_type = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

class Order(models.Model):
    def __str__(self):
        return f'{str(self.id)}'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, related_name='orders')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending')
    @property
    def total_cost(self):
        return sum(item.price for item in self.items.all())
    
class PnrDetail(models.Model):
    def __str__(self):
        return f'{str(self.pnr)}'
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    pnr = models.IntegerField(blank=True)
    start_location = models.CharField(max_length=20, default='')
    end_location = models.CharField(max_length=20, default='')