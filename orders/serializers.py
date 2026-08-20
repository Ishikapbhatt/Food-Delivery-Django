from .models import Order, OrderItem, Cart, CartItem
from rest_framework import serializers
from restaurants.serializers import RestaurantSerializer, MenuItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'subtotal', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    total = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'restaurant', 'items', 'total', 'total_items', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'price', 'subtotal', 'special_instructions']

class OrderCreationSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'delivery_address', 'delivery_phone', 'special_instructions', 'payment_method', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Calculate total amount
        total_amount = 0
        for item_data in items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
            quantity = item_data.get('quantity', 1)
            total_amount += menu_item.price * quantity
        
        validated_data['total_amount'] = total_amount
        validated_data['customer'] = user
        
        order = Order.objects.create(**validated_data)
        
        # Create order items
        for item_data in items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
            quantity = item_data.get('quantity', 1)
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=menu_item.price,
                special_instructions=item_data.get('special_instructions', '')
            )
        
        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_email', 'customer_name', 'restaurant', 'order_status', 
                  'payment_method', 'payment_status', 'total_amount', 'delivery_address', 'delivery_phone',
                  'special_instructions', 'estimated_delivery_time', 'actual_delivery_time', 'items', 
                  'created_at', 'updated_at']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status', 'estimated_delivery_time', 'actual_delivery_time']

class CartAddItemSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

class CartUpdateItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)