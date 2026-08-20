from django.db import models
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant, MenuItem

# Create your models here.

User = get_user_model()

class Order(models.Model):
    ORDER_STATUSES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("PREPARING", "Preparing"),
        ("READY", "Ready for Pickup"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
        ("REFUNDED", "Refunded"),
    )

    PAYMENT_METHODS = (
        ("CASH", "Cash on Delivery"),
        ("CARD", "Credit/Debit Card"),
        ("UPI", "UPI"),
        ("WALLET", "Wallet"),
    )

    PAYMENT_STATUSES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default=PAYMENT_METHODS[0][0])
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default=PAYMENT_STATUSES[0][0])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_address = models.TextField(blank=True, default='')
    delivery_phone = models.CharField(max_length=20, blank=True, default='')
    special_instructions = models.TextField(blank=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"<Order {self.id} by {self.customer.email}>"
    
    def calculate_total(self):
        total = sum(item.subtotal() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    special_instructions = models.TextField(blank=True)
    
    def subtotal(self):
        return self.price * self.quantity
    
    def __str__(self) -> str:
        return f"{self.menu_item.name} x {self.quantity}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.email}"
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())
    
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def subtotal(self):
        return self.menu_item.price * self.quantity
    
    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}" 