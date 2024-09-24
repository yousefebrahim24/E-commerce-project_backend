from django.urls import path 
from . import views 
from .views import uploadImage  

urlpatterns = [   
    path("products/" , views.get_products , name="get_all_products" )  ,
    path('product/<int:pk>/', views.get_product, name='get_single_product'),
    path("products/<int:pk>/" , views.get_product , name="get_product_by_pk" )  ,
    path("products/<int:pk>/update_product/" , views.update_product , name="update_product")  ,
    path("products/<int:pk>/delete_product/" , views.delete_product , name="delete_product")  ,
    path("categories/" , views.get_categories , name="get_categories" )  ,
    path("products/<int:pk>/reviews/" , views.get_product_reviews , name="get_product_reviews_by_pk" )  ,
    path("products/create/" , views.create_product , name="create_product" )  ,
    path("products/<int:pk>/create_review/" , views.create_review , name="create_review" )  ,
    path("products/<int:pk>/update_review/" , views.update_review , name="update_review" )  ,
    path("products/<int:pk>/delete_review/" , views.delete_review , name="delete_review" )  ,
    path("order/<int:pk>/" , views.get_order , name="get_order_by_pk" )  ,
    path('order/<int:pk>/', views.getOrderById, name='get_order_by_id'),
    path('order/<int:pk>/mark-paid/', views.updateOrderToPaid, name='update_order_to_paid'),
    path('my-orders/', views.getMyOrders, name='get_my_orders'),
    path('admin/orders/', views.getAllOrders, name='get_all_orders'),
    path('admin/order/<int:pk>/mark-delivered/', views.updateOrderToDelivered, name='update_order_to_delivered'),
    path("products/<int:pk>/delete/" , views.delete_product , name="delete_product_by_pk" )  ,
    path('product/<int:pk>/upload-image/', uploadImage, name='upload_image'),

]

