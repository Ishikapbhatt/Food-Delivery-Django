from django.urls import path
from . import views

urlpatterns = [
    path('cuisines/', views.CuisineListView.as_view(), name='cuisine-list'),
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/search/', views.search_restaurants, name='restaurant-search'),
    path('restaurants/<int:restaurant_id>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:restaurant_id>/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('restaurants/<int:restaurant_id>/categories/<int:category_id>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('restaurants/<int:restaurant_id>/menu/', views.MenuItemListView.as_view(), name='menu-item-list'),
    path('restaurants/<int:restaurant_id>/menu/<int:item_id>/', views.MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('restaurants/<int:restaurant_id>/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('restaurants/<int:restaurant_id>/reviews/<int:review_id>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('restaurants/<int:restaurant_id>/images/', views.RestaurantImageView.as_view(), name='restaurant-images'),
]