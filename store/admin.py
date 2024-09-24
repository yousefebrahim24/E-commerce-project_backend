from django.contrib import admin
from .models import Product , Order , Review , OrderItems , ShippingAddress
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register( ShippingAddress)
admin.site.register( OrderItems)