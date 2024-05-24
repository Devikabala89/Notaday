from django.contrib import admin
from notaday_app.models import products,contactus

# Register your models here.
#admin.site.register(products) #simply adds table in admin view to look more customized and easy below steps taken

#To make the table look more simplified in admin panel below steps are taken
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','category','is_active']  #predefined keywords
    list_filter=['category','is_active','price']

admin.site.register(products,ProductAdmin)

class contactAdmin(admin.ModelAdmin):
    list_display=['id','name','phone','email','msg']  #predefined keywords
  
admin.site.register(contactus,contactAdmin)