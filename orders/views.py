from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Order, OrderItem, Cart, CartItem
from restaurants.models import Restaurant, MenuItem

# Create your views here.

class CartView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartAddItemView(generics.GenericAPIView):
    serializer_class = serializers.CartAddItemSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            menu_item_id = serializer.validated_data['menu_item_id']
            quantity = serializer.validated_data['quantity']
            
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id, is_available=True)
            except MenuItem.DoesNotExist:
                return Response({'error': 'Menu item not found or unavailable'}, status=status.HTTP_404_NOT_FOUND)
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Check if cart has items from another restaurant
            if cart.restaurant and cart.restaurant != menu_item.restaurant:
                return Response({'error': 'Cannot add items from different restaurant. Clear cart first.'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Set restaurant if cart is new
            if not cart.restaurant:
                cart.restaurant = menu_item.restaurant
                cart.save()
            
            # Add or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                menu_item=menu_item,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            cart_serializer = serializers.CartSerializer(cart)
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartUpdateItemView(generics.GenericAPIView):
    serializer_class = serializers.CartUpdateItemSerializer
    permission_classes = [IsAuthenticated]
    
    def put(self, request, item_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
                cart_item.quantity = serializer.validated_data['quantity']
                cart_item.save()
                
                cart_serializer = serializers.CartSerializer(cart_item.cart)
                return Response(cart_serializer.data, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartRemoveItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            
            # Check if cart is empty and reset restaurant
            cart = cart_item.cart
            if cart.items.count() == 0:
                cart.restaurant = None
                cart.save()
            
            cart_serializer = serializers.CartSerializer(cart)
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

class CartClearView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            cart.restaurant = None
            cart.save()
            
            cart_serializer = serializers.CartSerializer(cart)
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderCreateListView(generics.ListCreateAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.OrderCreationSerializer
        return serializers.OrderDetailSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Clear the cart after order creation
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            cart.restaurant = None
            cart.save()
        except Cart.DoesNotExist:
            pass
        
        return Response(serializers.OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.OrderStatusUpdateSerializer
        return serializers.OrderDetailSerializer

class UserOrderView(generics.ListAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)