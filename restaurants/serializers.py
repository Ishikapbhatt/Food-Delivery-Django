from rest_framework import serializers
from .models import Cuisine, Restaurant, Category, MenuItem, Review, RestaurantImage

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = '__all__'

class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    cuisine_names = serializers.SerializerMethodField()
    images = RestaurantImageSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Restaurant
        fields = '__all__'
    
    def get_cuisine_names(self, obj):
        return [cuisine.name for cuisine in obj.cuisine.all()]

class RestaurantDetailSerializer(RestaurantSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = '__all__'
    
    def get_reviews(self, obj):
        recent_reviews = obj.reviews.all()[:10]
        return ReviewSerializer(recent_reviews, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
    
    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        review.restaurant.update_rating()
        return review
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        instance.restaurant.update_rating()
        return instance