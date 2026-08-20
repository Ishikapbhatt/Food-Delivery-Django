from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import Cuisine, Restaurant, Category, MenuItem, Review, RestaurantImage
from .serializers import (
    CuisineSerializer, RestaurantSerializer, RestaurantDetailSerializer,
    CategorySerializer, MenuItemSerializer, ReviewSerializer, RestaurantImageSerializer
)

class CuisineListView(generics.ListAPIView):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RestaurantListView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cuisine', 'price_range', 'is_featured']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['name', 'average_rating', 'created_at']
    ordering = ['-average_rating']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Restaurant.objects.filter(is_active=True)

class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Category.objects.filter(restaurant_id=restaurant_id)
    
    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_id')
        serializer.save(restaurant_id=restaurant_id)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'category_id'
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Category.objects.filter(restaurant_id=restaurant_id)

class MenuItemListView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        category_id = self.kwargs.get('category_id')
        queryset = MenuItem.objects.filter(restaurant_id=restaurant_id, is_available=True)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_id')
        serializer.save(restaurant_id=restaurant_id)

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'item_id'
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return MenuItem.objects.filter(restaurant_id=restaurant_id)

class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Review.objects.filter(restaurant_id=restaurant_id)
    
    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_id')
        serializer.save(user=self.request.user, restaurant_id=restaurant_id)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'review_id'
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Review.objects.filter(restaurant_id=restaurant_id, user=self.request.user)

class RestaurantImageView(generics.ListCreateAPIView):
    serializer_class = RestaurantImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return RestaurantImage.objects.filter(restaurant_id=restaurant_id)
    
    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_id')
        serializer.save(restaurant_id=restaurant_id)

@swagger_auto_schema(method='get', operation_description="Search restaurants by name, cuisine, or location")
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_restaurants(request):
    query = request.GET.get('q', '')
    cuisine = request.GET.get('cuisine', '')
    price_range = request.GET.get('price_range', '')
    
    restaurants = Restaurant.objects.filter(is_active=True)
    
    if query:
        restaurants = restaurants.filter(name__icontains=query) | restaurants.filter(description__icontains=query)
    
    if cuisine:
        restaurants = restaurants.filter(cuisine__name__icontains=cuisine)
    
    if price_range:
        restaurants = restaurants.filter(price_range=price_range)
    
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)