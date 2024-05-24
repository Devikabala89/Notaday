from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class products(models.Model):
    name=models.CharField(max_length=50)
    category=models.CharField(max_length=60)
    price=models.FloatField()
    is_active=models.BooleanField(default=True,verbose_name="Availablility")
    pdetails=models.CharField(max_length=150)
    pimage=models.ImageField(upload_to='image')
    #def __str__(self):
    #    return self.name   #based on name show the entries in admin panel

class cart(models.Model):
    #id is added default
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(products,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(products,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order_history(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(products,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Todo(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    task=models.CharField(max_length=150)
    date=models.DateField()
    status=models.CharField(max_length=20)
    importance=models.CharField(max_length=10)

class Notes(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    title=models.CharField(max_length=250)
    note=models.CharField(max_length=1500)
    
class contactus(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    msg=models.CharField(max_length=300)

class Calorietracker(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    date=models.DateField()
    cat=models.CharField(max_length=50)
    aim=models.IntegerField()
    food=models.CharField(max_length=100)
    intake=models.IntegerField()