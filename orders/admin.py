from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'restaurant', 'order_status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['order_status', 'payment_status', 'payment_method', 'created_at', 'restaurant']
    search_fields = ['customer__email', 'customer__username', 'restaurant__name']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'price', 'subtotal']
    list_filter = ['order', 'menu_item']
    search_fields = ['menu_item__name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'total_items', 'created_at']
    list_filter = ['restaurant', 'created_at']
    search_fields = ['user__email', 'user__username']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'menu_item', 'quantity', 'subtotal']
    list_filter = ['cart', 'menu_item']
    search_fields = ['menu_item__name']