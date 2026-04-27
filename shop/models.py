from django.db import models
from django.contrib.auth.models import User 
import datetime 
import os


def getFilename(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%M%d%H:%M:%S")
    new_filename ="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)    

class Catagory(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFilename,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show, 1-hidden")
    created_at=models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
         return self.name


   

class Product(models.Model):

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
    )

    CARAT_CHOICES = (
        (18, '18 Carat'),
        (22, '22 Carat'),
        (24, '24 Carat'),
        (925, '925 Sterling Silver'),
        (1, '1.15 Carat'),
        (1, '1.50 Carat'),
        (1, '1.85 Carat'),
        (2, '2.25 Carat'),
        (3, '3.05 Carat'),
        (3, '3.50 Carat'),
        (4, '4.20 Carat'),
        (4, '4.65 Carat'),
        (5, '5.50 Carat'),
        (6, '6.25 Carat'),
        (6, '6.85 Carat'),
        (8, '8.20 Carat'),
        (12, '12.50 Carat'),
        (15, '15.00 Carat'),
)

    
    Catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)

    # Basic details
    name = models.CharField(max_length=200,null=False,blank=False)
    
    product_image=models.ImageField(upload_to=getFilename,null=True,blank=True)

    description=models.TextField(max_length=500,null=False,blank=False)


    # Jewellery details
    carat = models.IntegerField(choices=CARAT_CHOICES,blank=True,null=True)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        help_text="Weight of jewel in grams"
    )

    wastage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Wastage percentage"
    )

    # Price calculation
    price_without_wastage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Price without wastage"
    )

    price_add_wastage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Price including wastage"
    )
    quantity = models.PositiveIntegerField(default=10,blank=False,null=False)


    # Product status
    trending = models.BooleanField(default=False,help_text="0-default,1-Trending")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  created_at=models.DateTimeField(auto_now_add=True)

  @property
  def total_cost(self):
    return self.product_qty * self.product.price_add_wastage


class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


class Order(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=150) 
    email = models.EmailField(max_length=150) 
    phone = models.CharField(max_length=20) 
    address = models.TextField() 
    city = models.CharField(max_length=150) 
    state = models.CharField(max_length=150) 
    country = models.CharField(max_length=150) 
    total_amount = models.FloatField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self): 
        return f"Order #{self.id}"


class OrderItem(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    product = models.ForeignKey("Product", on_delete=models.CASCADE) 
    quantity = models.IntegerField() 
    price = models.FloatField() 
    total = models.FloatField() 
    order_number = models.CharField(max_length=20, null=True) 
    payment_mode = models.CharField(max_length=50, default="Cash On Delivery") 
    payment_status = models.CharField(max_length=50, default="Pending") 
    ordered_date = models.DateTimeField(null=True) 


    def __str__(self): 
        return f"{self.order.id} - {self.product.name}"



class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]



class WastagePrediction(models.Model):
    jewel_type = models.CharField(max_length=100)
    karat = models.IntegerField()
    design_type = models.CharField(max_length=100)
    stone_included = models.BooleanField()
    gold_given_weight = models.FloatField()
    final_weight = models.FloatField()
    predicted_wastage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.jewel_type
    

class MarketRate(models.Model):
    gold_price = models.FloatField()
    silver_price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - Gold ₹{self.gold_price}"
    

class SearchHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class CartHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductViewHistory(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    viewed_at = models.DateTimeField(auto_now_add=True)