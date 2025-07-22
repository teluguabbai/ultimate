from django.db import models



# Create your models here.
class webpagedata(models.Model):
    web_name=models.CharField(max_length=50)
    web_email=models.EmailField( max_length=254)
    web_phone=models.IntegerField(max_length=10)
    web_message = models.TextField(max_length=250)

class androidData(models.Model):
    name= models.CharField( max_length=50)
    email= models.EmailField(max_length=254)
    phone = models.IntegerField(max_length=10)
    message = models.TextField(max_length=250)
    


class SmartHomeProduct(models.Model):
    CATEGORY_CHOICES = [
        ('switch', 'Smart Switch'),
        ('sensor', 'Smart Sensor'),
        ('module', 'Smart Module'),
        ('other', 'Other Smart Devices')
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    


class Property(models.Model):
    name = models.CharField(max_length=200, default="Unnamed Property")  # ✅ Corrected field
    mobile = models.CharField(max_length=15, default="0000000000")  # ✅ Corrected field
    address = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    url=models.URLField( max_length=200)


    def __str__(self):
        return self.name


#payments database
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Paid", "Paid")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"
    
#car rental

from django.core.validators import *
from django.contrib.auth.models import User

# Create your models here.


class Area(models.Model):
    pincode = models.CharField(validators = [MinLengthValidator(6), MaxLengthValidator(6)],max_length = 6,unique=True)
    city = models.CharField(max_length = 20)

class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.OneToOneField(Area, on_delete=models.PROTECT)
    wallet = models.IntegerField(default = 0)

class Vehicles(models.Model):
    car_name = models.CharField(max_length = 20)
    color = models.CharField(max_length = 10)
    dealer = models.ForeignKey(CarDealer, on_delete = models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null = True)
    capacity = models.CharField(max_length = 2)
    is_available = models.BooleanField(default = True)
    description = models.CharField(max_length = 100)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    days = models.CharField(max_length = 3)
    is_complete = models.BooleanField(default = False)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)





