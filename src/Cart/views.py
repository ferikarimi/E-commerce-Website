from django.shortcuts import redirect , get_object_or_404  , get_list_or_404
from rest_framework.permissions import IsAuthenticated , AllowAny
from Vendors.permissions import IsAuthenticatedVendor 
from rest_framework.views import APIView
from rest_framework.response import Response
from Products.models import Product 
from Customers.models import Addresses
from .models import OrderDetail , Orders
from .serializers import UserOrderSerializer , VendorOrderSerializer , UserOrderDetailSerializer
from Products.models import Shop
import json



class Cart (APIView):
    """
        create, get and update pre shopping cart with cookies
    """
    permission_classes = [AllowAny]
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


class CheckOutView (APIView):
    """
        finalize shopping cart and register cart to database
    """
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
        address_id = request.data.get('address_id')
        address =get_object_or_404(Addresses , id=address_id , user=request.user)
        total_price = 0

        if not cart :
            return Response({'message':'your cart is empty'} , status=400)
    
        if not address :
            return Response({'error':'you dont choice any addresss'})

        for item in cart.values():
            total_price += float(item['price'] * item['quantity'])
        
        order = Orders.objects.create(
            customer=request.user , 
            address = address ,
            status = 'pending',
            total_price = total_price ,
            discount_price = 0 ,
            )
        
        print('cart:', cart)
        for product_id, item in cart.items():
            product = get_object_or_404(Product , id=int(product_id))
            print('product_id:', product_id)
            print('item:', item)

            if product.stock < item['quantity'] :
                return Response ({'message':f'not enugh stock for {product.name}'},status=400)
            
            print(f"quantity type: {type(item['quantity'])}, value: {item['quantity']}")
            product.stock -= item['quantity']
            product.sold_count += item['quantity']
            product.save()
            print(f"Updated product {product.id}: stock={product.stock}, sold_count={product.sold_count}")

            OrderDetail.objects.create(
                product = product ,
                order = order ,
                single_price = item['price'] ,
                quantity = item['quantity']
            )

        response = Response({'message':'order finalized successfully.'}, status=201)
        self.set_cart(response , {})
        return response


class UserOrdersView (APIView):
    """
        get user orders 
    """
    permission_classes = [IsAuthenticated]

    def get (self , request):
        user = request.user
        orders = Orders.objects.filter(customer=user).order_by('-order_date')
        serializer = UserOrderSerializer (orders , many=True)
        return Response (serializer.data , status=200)
    
    def delete (self , request , id):
        user = request.user
        order = get_object_or_404(Orders , id=id , customer=user)
        
        if order.status in ['cancelled' , 'delivered'] :
            return Response ({'error':'you can not cancelled an order that already cancelled or delivered'}, status=400)

        order.status = 'cancelled'
        order.save()
        return Response({'message':'order cancelled successfully !'})


class UserOrderDetail(APIView):
    """
        get user order details
    """
    def get(self, request):
        user= request.user
        order = get_list_or_404(Orders , customer=user)
        order_detail = OrderDetail.objects.filter(order__in=order)
        serializer = UserOrderDetailSerializer(order_detail , many=True)
        return Response(serializer.data , status=200)


class VendorOrdersView (APIView):
    """
        get shop`s orders and change order status
    """
    permission_classes = [IsAuthenticatedVendor]

    def get (self , request):
        vendor = request.user.vendors
        vendor_products = Product.objects.filter(store_name__vendor=vendor)
        order_detail = OrderDetail.objects.filter(product__in=vendor_products)
        orders = Orders.objects.filter(order__in=order_detail).order_by('-order_date')

        serializer = VendorOrderSerializer (orders , many=True)
        return Response (serializer.data , status=200)
    
    def put (self , request , id):
        vendor = request.user.vendors
        shop = get_object_or_404(Shop , vendor=vendor)
        order = get_object_or_404 (Orders , id=id)
        access = OrderDetail.objects.filter(order=order , product__store_name=shop).exists()
        if not access :
            return Response({'error':'you can not access to this order!'} , status=403)
        
        serializer = VendorOrderSerializer(order , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data , status=200)
        return Response (serializer.errors , status=400)