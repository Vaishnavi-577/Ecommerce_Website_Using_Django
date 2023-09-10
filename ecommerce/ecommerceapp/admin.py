from django.contrib import admin

# Register your models here.
#after creating the models and making migrations should register it into the administration
#to reflect it into the backend
#python manage.py makemigrations
#python manage.py migrate 

from ecommerceapp.models import Contact
from ecommerceapp.models import Product,Orders,OrderUpdate
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
