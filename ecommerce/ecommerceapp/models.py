from django.db import models

# Create your models here.
#Database tables are created here 
# any changes are done into the models migrations should apply

class Contact(models.Model):
    #contact table is created
    #impliocitly in django one primary key will be alloted 
    # if wanted to do explicitly the 
    #contact_id.CharField(max_length=50) becomes primary key
    
    
    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField()
    
    def __str__(self):
        return self.name
    
#pillow have to installed in django to support images pip install pillow in terminal/cmd
   
class Product(models.Model):
    product_id=models.AutoField 
    #by Autofield it creates a random id 
    product_name=models.CharField(max_length=100)
    category=models.CharField(max_length=100,default='')
    subcategory=models.CharField(max_length=50,default='')
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    
    image=models.ImageField(upload_to='images',default='')
    
    #here pics and all the details mentioned above can be directly added from the administration
    #check also the urls in ecommereapp where i have include the media when i added images 
    #from the administration the pics will get uploaded into the media folder
    
    def __str__(self):
        return self.product_name
    
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json =  models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)    
    oid=models.CharField(max_length=150,blank=True)
    amountpaid=models.CharField(max_length=500,blank=True,null=True)
    paymentstatus=models.CharField(max_length=20,blank=True)
    phone = models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name   

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered=models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."     
    
    
    
    
    
