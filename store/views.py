from rest_framework.decorators import api_view 
from .models import Product  , Review , Order
from .serializers import ProductSerializer , ReviewSerializer , OrderSerializer
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import BasePermission ,  IsAuthenticated , IsAdminUser
from rest_framework.decorators import permission_classes
from django.utils import timezone


# authentication
    # know who you are (username, password)
# authorization 
    # do you have permission to do so ?
class MyAuthentication(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = request.user 
        if user.first_name != "mohamed" :
            return True 
        else : 
            return False
        # return 
@api_view(["GET"])
def get_categories(request) :
    categories = Product.objects.values("category").distinct()
    return Response({"data" : list(categories)})
    
# @permission_classes([MyAuthentication])
@api_view(["GET"])
def get_product(request, pk):
    try:
        product = Product.objects.get(id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error occurred: {e}")
        return Response({'error': 'Product not found or another error occurred'}, status=status.HTTP_400_BAD_REQUEST)  
    

# @api_view(["GET"])
# def get_products(request) : 
#     # print(request.user)
#     try : 
#         q = request.GET.dict() 
#         category = q.get("category" , "")
#         print(category)
#         products = Product.objects.filter(category__contains = category) 
        
#         serializer = ProductSerializer(products , many = True)
        
#         return Response(serializer.data , status=status.HTTP_200_OK)
    
#     except : 
#         return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_products(request):
    try :
        products = Product.objects.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data,status= status.HTTP_200_OK)
    except Exception as ex:
        return Response({'error':f'error happend {ex}'},status= status.HTTP_400_BAD_REQUEST)
 
@api_view(["GET"]) 
@permission_classes([IsAdminUser])
def get_product(request , pk) : 
    try : 
        product = Product.objects.get(id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data  , status=200)
    except Product.DoesNotExist : 
        return Response(status=404)
    except : 
        return Response(status=400)
    
# @api_view(["PUT"]) 
# @permission_classes([IsAuthenticated,IsAdminUser])
# def update_product(request , pk) : 
#     try : 
#         product = Product.objects.get(id = pk)
#         serializer = ProductSerializer(product , data=request.data)
#         return Response(serializer.data  , status=200)
#     except Product.DoesNotExist : 
#         return Response(status=404)
#     except : 
#         return Response(status=400)
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return Response({"message": "Product deleted successfully."}, status=200)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    



@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_product_reviews(request , pk) : 
    try : 
        reviews = Review.objects.filter(product_id = pk ) 
        serializer = ReviewSerializer(reviews , many = True) 
        print(serializer.data)
        return Response(serializer.data , status=200)
    except :
        return Response(status=400)

@api_view(["GET"])    
def get_order(request , pk): 
    try : 
        order = Order.objects.get(id = pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist :
        return Response(status=404)
    except Exception as ex : 
        return Response(str(ex) ,  status=400)
         
@api_view(['GET'])
@permission_classes([IsAuthenticated , IsAdminUser])
def getOrderById(request, pk):
    try:
        # Retrieve the order by ID
        order = Order.objects.get(id=pk)
        
        # Check if the user is either the owner of the order or an admin
        if request.user == order.user or request.user.is_staff:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)       

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    try:
        # Retrieve the order by ID
        order = Order.objects.get(id=pk)
        
        # Check if the user is the owner of the order
        if request.user != order.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Update the order to paid
        order.is_paid = True
        order.paid_at = timezone.now()
        order.save()
        
        return Response({'detail': 'Order updated to paid'}, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    try:
        # Retrieve all orders associated with the authenticated user
        orders = Order.objects.filter(user=request.user)
        
        # Serialize the order data
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as ex:
        return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllOrders(request):
    try:
        # Retrieve all orders in the system
        orders = Order.objects.all()
        
        # Serialize the order data
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as ex:
        return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    try:
        # Retrieve the order by ID
        order = Order.objects.get(id=pk)
        
        # Update the order to delivered
        order.is_delivered = True
        order.delivered_at = timezone.now()
        order.save()
        
        return Response({'detail': 'Order updated to delivered'}, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product(request) : 
    user = request.user 
    data = request.data 
    data["user"] = user.id 
    try : 
        serializer =  ProductSerializer(data = data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors , status=400)
    except Exception as ex :
        return Response({"details" : f"error happen {str(ex)}"} , status=400) 
    

    # for image
@api_view(['POST'])
def uploadImage(request, pk):
    try:
        product = Product.objects.get(id=pk)
        
        # Check if an image file is included in the request
        if 'image' not in request.FILES:
            return Response({'detail': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the product's image field
        product.image = request.FILES['image']
        product.save()
        
        # Serialize and return the updated product data
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request , pk) : 
    data = request.data 
    data["product"] = pk 
    data["user"] = request.user.id 
    serializer = ReviewSerializer(data = data)
    if serializer.is_valid() : 
        serializer.save()
        return Response(serializer.data , status=201)
    else : 
        return Response(serializer.errors , status=400)


class ReviewAuthentication(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs["pk"]
        review = Review.objects.get(id = pk)
        user_id= review.user_id 
        user = request.user
        if user_id == user.id :
            return True 
        else : 
            return False
        
@api_view(["PUT"])
@permission_classes([ReviewAuthentication])
def update_review(request , pk) : 
    data = request.data 
    review = Review.objects.get(id = pk)
    
    data["user"] = review.user_id
    data["product"] = review.product_id
    
    serializer = ReviewSerializer(data=data , instance = review )
    if serializer.is_valid() : 
        serializer.save() 
        return Response(serializer.data , status=200)
    else : 
        return Response(serializer.errors , status=400)
    # return Response(data)
    
@api_view(["DELETE"])
@permission_classes([ReviewAuthentication])
def delete_review(request , pk) : 
    try : 
        Review.objects.filter(id = pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as ex : 
        return Response({"detail" : f"error happen {str(ex)}"} , status=400)


