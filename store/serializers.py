from rest_framework import serializers 
from .models import Product , Review , Order , ShippingAddress , OrderItems

class ReviewSerializer(serializers.ModelSerializer) : 
    product_name = serializers.SerializerMethodField(read_only = True)
    # product_image = serializers.SerializerMethodField(read_only = True)
    
    # def get_product_image(self , obj) : 
    #     return obj.product.image.url
    
    def get_product_name(self , obj) : 
        return obj.product.name
    class Meta : 
        model = Review
        fields = "__all__"
        # fields = ["__all__"]
    
    
class ProductSerializer(serializers.ModelSerializer) :
  
    class Meta : 
        model = Product
        fields = "__all__"
        
    
    def get_reviews(self , obj) : 
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews , many = True)
        return serializer.data
    reviews = serializers.SerializerMethodField(read_only = True)


class ShippingAddressSerializer(serializers.ModelSerializer) :
        class Meta :
            model = ShippingAddress 
            fields = "__all__"

class OrderItemsSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = OrderItems
        fields = ["product" , "quantity" , "price"]

from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = User
        fields = ["username" , "first_name" , "last_name" , "is_superuser" , "is_staff"]
  
class OrderSerializer(serializers.ModelSerializer) : 
    user_data = serializers.SerializerMethodField(read_only = True)
    
    def get_user_data(self , obj) : 
        
        user = obj.user 
        if user : 
            serializer = UserSerializer(user)
            return serializer.data 
        
        else : 
            return {}
        
    
    order_items = serializers.SerializerMethodField(read_only = True)
    
    def get_order_items(self , obj) : 
        order_items = obj.order_items.all()
        serializer  = OrderItemsSerializer(order_items , many = True)
        return serializer.data
    
    
    shipping_address = serializers.SerializerMethodField(read_only = True)
    
    def get_shipping_address(self , obj) : 
        # print("hello")
        if hasattr(obj ,"shipping_address" ) :
            address = obj.shipping_address 
        else : 
            return {}
 
        serializer = ShippingAddressSerializer(address)
        return serializer.data
        
    class Meta : 
        model = Order 
        fields = "__all__"
