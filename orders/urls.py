from django.urls import path
from . import views


urlpatterns = [
    # Cart endpoints
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add-item/", views.CartAddItemView.as_view(), name="cart_add_item"),
    path("cart/update-item/<int:item_id>/", views.CartUpdateItemView.as_view(), name="cart_update_item"),
    path("cart/remove-item/<int:item_id>/", views.CartRemoveItemView.as_view(), name="cart_remove_item"),
    path("cart/clear/", views.CartClearView.as_view(), name="cart_clear"),
    
    # Order endpoints
    path("", views.OrderCreateListView.as_view(), name="orders"),
    path("<int:order_id>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("my-orders/", views.UserOrderView.as_view(), name="my_orders"),
]