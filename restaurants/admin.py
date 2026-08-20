from django.contrib import admin
from .models import Cuisine, Restaurant, Category, MenuItem, Review, RestaurantImage

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'price_range', 'average_rating', 'total_reviews', 'is_active', 'is_featured']
    list_filter = ['price_range', 'is_active', 'is_featured', 'cuisine']
    search_fields = ['name', 'owner__username', 'address']
    inlines = [CategoryInline, MenuItemInline, RestaurantImageInline]
    filter_horizontal = ['cuisine']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'order']
    list_filter = ['restaurant']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price', 'is_available', 'is_vegetarian']
    list_filter = ['restaurant', 'category', 'is_available', 'is_vegetarian', 'is_spicy']
    search_fields = ['name', 'description']
    ordering = ['restaurant', 'order']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'rating', 'created_at']
    list_filter = ['rating', 'restaurant', 'created_at']
    search_fields = ['user__username', 'restaurant__name', 'comment']

@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'order', 'caption']
    list_filter = ['restaurant']
    search_fields = ['caption']