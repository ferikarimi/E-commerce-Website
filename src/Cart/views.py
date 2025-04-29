from django.shortcuts import redirect , get_object_or_404
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
from rest_framework.response import Response
from Products.models import Product 
from Customers.models import Addresses
from .models import OrderDetail , Orders
import json

# Create your views here.


#___________________________ cart with cookies ______________________________________
class Cart (APIView):
    def get_cart (self , request):
        cart = request.COOKIES.get('cart')
        if cart :
            try :
                return json.loads(cart)
            except json.JSONDecodeError :
                return {}
        return {}
        
    def set_cart (self , response , cart):
        response.set_cookie('cart',json.dumps(cart) , max_age = 300 )
    
    def get (self , request):
        cart = self.get_cart(request)
        cart_items = []
        products_id = cart.keys()
        products = Product.objects.filter(id__in=products_id)

        for product in products :
            product_id = str (product.id)
            item = cart[product_id]
            cart_items.append({
                'product_id': product.id ,
                'name': product.name ,
                'price': item['price'] ,
                'quantity': item['quantity'] ,
                'total_price': float(item['price'] * item['quantity']) ,
            }) 
        
        total_cart_price = sum(item['total_price'] for item in cart_items)
        return Response({
            'cart_items' : cart_items ,
            'total_cart_price' : total_cart_price
        })
    
    def post (self , request) :
        product_id = str(request.data.get('product_id'))
        quantity = int(request.data.get('quantity' ,1))
        product = get_object_or_404(Product , id=product_id)
        cart = self.get_cart(request)
        if product_id in cart :
            cart[product_id]['quantity'] += quantity
        else :
            cart[product_id] = {
                'quantity':quantity ,
                'price': float(product.price)
            }
        response = Response({'message':'product added to cart'} , status=200)
        self.set_cart(response , cart)
        return response

    def put (self , request):
        product_id = str(request.data.get('product_id'))
        action = request.data.get('action')
        cart = self.get_cart(request)
        if product_id not in cart :
            return Response({'message':'item does not in your cart !'})
        if action == 'increase' :
            cart[product_id]['quantity'] += 1
        elif action == 'decrease' :
            if cart[product_id]['quantity'] > 1 :
                cart[product_id]['quantity'] -= 1
            else :
                cart.pop(product_id)
        elif action == 'remove' :
            cart.pop(product_id)
        else :
            return Response({'message':'invalid'} , status=400)
        response = Response({'message':'cart updated'} , status=200)
        self.set_cart(response , cart)
        return response
















class FinalCart (APIView):
    permission_classes = [IsAuthenticated]

    def get_cart (self , request):
        cart = request.COOKIES.get('cart')
        if cart :
            try :
                return json.loads(cart)
            except json.JSONDecodeError :
                return {}
        return {}
        
    def set_cart (self , response , cart):
        response.set_cookie('cart',json.dumps(cart) , max_age = 300 )

    
    def get (self , request):
        if not request.user.is_authenticated :
            return redirect ('login')
        
        return redirect('/customer/address/')
    
    def post (self , request):
        cart = self.get_cart(request)
        if not cart :
            return Response({'message':'your cart is empty'} , status=400)
        
        address_id = request.data.get('address_id')
        address =get_object_or_404(Addresses , id=address_id , user=request.user)

        total_price = 0
        for item in cart.values():
            total_price += float(item['price'] * item['quantity'])
        
        order = Orders.objects.create(
            customer=request.user , 
            address = address ,
            status = 'pending',
            total_price = total_price ,
            discount_price = 0 ,
            )

        for product_id in cart.keys():
            product = get_object_or_404(Product , id=product_id)

            if product.stock < item['quantity'] :
                return Response ({'message':f'not enugh stock for {product.name}'},status=400)
            product.stock -= item['quantity']
            product.save()

            OrderDetail.objects.create(
                product = product ,
                order = order ,
                single_price = item['price'] ,
                quantity = item['quantity']
            )

        response = Response({'message':'order finalized successfully.'}, status=201)
        self.set_cart(response , {})
        return response


































#_____________________ cookie _________________________
# def set_cookie(request):
#     response = HttpResponse("cookie set!")
#     response.set_cookie('username','djangoMaster')
#     return response

# def get_cookie(request):
#     username = request.COOKIES.get('username','guest')
#     return HttpResponse(f'hello {username}')

# def delete_cookie(request):
#     response = HttpResponse('cooki delete successfuly!')
#     response.delete_cookie('username')
#     return response