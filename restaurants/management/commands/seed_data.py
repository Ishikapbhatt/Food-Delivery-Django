from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from restaurants.models import Cuisine, Restaurant, Category, MenuItem, RestaurantImage
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed sample data for the food delivery application'

    def handle(self, *args, **options):
        self.stdout.write('Seeding sample data...')
        
        # Create cuisines
        cuisines_data = [
            {'name': 'Italian', 'description': 'Italian cuisine'},
            {'name': 'Chinese', 'description': 'Chinese cuisine'},
            {'name': 'Indian', 'description': 'Indian cuisine'},
            {'name': 'Mexican', 'description': 'Mexican cuisine'},
            {'name': 'American', 'description': 'American cuisine'},
            {'name': 'Japanese', 'description': 'Japanese cuisine'},
        ]
        
        cuisines = []
        for cuisine_data in cuisines_data:
            cuisine, created = Cuisine.objects.get_or_create(
                name=cuisine_data['name'],
                defaults={'description': cuisine_data['description']}
            )
            cuisines.append(cuisine)
            if created:
                self.stdout.write(f'Created cuisine: {cuisine.name}')
        
        # Create a restaurant owner
        owner, created = User.objects.get_or_create(
            email='restaurant@foodie.com',
            defaults={
                'username': 'restaurant_owner',
                'phone_number': '+1234567890',
                'is_staff': True,
            }
        )
        if created:
            owner.set_password('password123')
            owner.save()
            self.stdout.write('Created restaurant owner user')
        
        # Create sample restaurants
        restaurants_data = [
            {
                'name': 'Bella Italia',
                'description': 'Authentic Italian cuisine with a modern twist. Fresh pasta, wood-fired pizzas, and traditional recipes passed down through generations.',
                'address': '123 Main Street, Downtown',
                'phone_number': '+1234567890',
                'email': 'info@bellaitalia.com',
                'price_range': '$$',
                'is_featured': True,
                'opening_time': '11:00:00',
                'closing_time': '22:00:00',
                'image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800',
                'cover_image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200',
                'cuisines': ['Italian']
            },
            {
                'name': 'Dragon Palace',
                'description': 'Exquisite Chinese cuisine featuring Szechuan and Cantonese specialties. Fresh ingredients and authentic flavors.',
                'address': '456 Oak Avenue, Chinatown',
                'phone_number': '+1234567891',
                'email': 'info@dragonpalace.com',
                'price_range': '$$',
                'is_featured': True,
                'opening_time': '10:00:00',
                'closing_time': '23:00:00',
                'image': 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800',
                'cover_image': 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=1200',
                'cuisines': ['Chinese']
            },
            {
                'name': 'Spice Garden',
                'description': 'Traditional Indian cuisine with rich spices and aromatic dishes. From curries to tandoori specialties.',
                'address': '789 Curry Lane, Little India',
                'phone_number': '+1234567892',
                'email': 'info@spicegarden.com',
                'price_range': '$',
                'is_featured': False,
                'opening_time': '11:00:00',
                'closing_time': '22:30:00',
                'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800',
                'cover_image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=1200',
                'cuisines': ['Indian']
            },
            {
                'name': 'Taco Fiesta',
                'description': 'Vibrant Mexican cuisine with street tacos, burritos, and fresh guacamole. A fiesta of flavors!',
                'address': '321 Fiesta Road, Latin Quarter',
                'phone_number': '+1234567893',
                'email': 'info@tacofiesta.com',
                'price_range': '$',
                'is_featured': False,
                'opening_time': '10:30:00',
                'closing_time': '21:00:00',
                'image': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800',
                'cover_image': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=1200',
                'cuisines': ['Mexican']
            },
            {
                'name': 'Burger Barn',
                'description': 'Classic American burgers and comfort food. Juicy patties, crispy fries, and milkshakes.',
                'address': '555 Burger Boulevard, Food Court',
                'phone_number': '+1234567894',
                'email': 'info@burgerbarn.com',
                'price_range': '$',
                'is_featured': True,
                'opening_time': '11:00:00',
                'closing_time': '23:00:00',
                'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800',
                'cover_image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=1200',
                'cuisines': ['American']
            },
            {
                'name': 'Sakura Sushi',
                'description': 'Authentic Japanese sushi and sashimi. Fresh fish delivered daily and prepared by master chefs.',
                'address': '888 Sushi Street, Japan Town',
                'phone_number': '+1234567895',
                'email': 'info@sakurasushi.com',
                'price_range': '$$$',
                'is_featured': False,
                'opening_time': '12:00:00',
                'closing_time': '22:00:00',
                'image': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800',
                'cover_image': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=1200',
                'cuisines': ['Japanese']
            }
        ]
        
        for restaurant_data in restaurants_data:
            cuisine_names = restaurant_data.pop('cuisines')
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_data['name'],
                defaults={
                    **restaurant_data,
                    'owner': owner
                }
            )
            
            if created:
                # Add cuisines
                for cuisine_name in cuisine_names:
                    try:
                        cuisine = Cuisine.objects.get(name=cuisine_name)
                        restaurant.cuisine.add(cuisine)
                    except Cuisine.DoesNotExist:
                        pass
                
                restaurant.save()
                self.stdout.write(f'Created restaurant: {restaurant.name}')
                
                # Create categories and menu items
                self.create_menu_items(restaurant)
            else:
                self.stdout.write(f'Restaurant already exists: {restaurant.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data seeded successfully!'))

    def create_menu_items(self, restaurant):
        menu_templates = {
            'Italian': [
                {'category': 'Appetizers', 'items': [
                    {'name': 'Bruschetta', 'description': 'Toasted bread topped with fresh tomatoes, garlic, and basil', 'price': 8.99, 'vegetarian': True},
                    {'name': 'Caprese Salad', 'description': 'Fresh mozzarella, tomatoes, and basil with balsamic glaze', 'price': 10.99, 'vegetarian': True},
                ]},
                {'category': 'Pasta', 'items': [
                    {'name': 'Spaghetti Carbonara', 'description': 'Classic pasta with eggs, cheese, pancetta, and black pepper', 'price': 16.99, 'vegetarian': False},
                    {'name': 'Fettuccine Alfredo', 'description': 'Creamy parmesan sauce over fresh fettuccine', 'price': 15.99, 'vegetarian': True},
                ]},
                {'category': 'Pizza', 'items': [
                    {'name': 'Margherita', 'description': 'Fresh mozzarella, tomatoes, and basil on wood-fired crust', 'price': 14.99, 'vegetarian': True},
                    {'name': 'Pepperoni', 'description': 'Classic pepperoni with mozzarella and tomato sauce', 'price': 16.99, 'vegetarian': False},
                ]}
            ],
            'Chinese': [
                {'category': 'Appetizers', 'items': [
                    {'name': 'Spring Rolls', 'description': 'Crispy rolls filled with vegetables', 'price': 7.99, 'vegetarian': True},
                    {'name': 'Dim Sum Platter', 'description': 'Assorted steamed dumplings', 'price': 12.99, 'vegetarian': False},
                ]},
                {'category': 'Main Course', 'items': [
                    {'name': 'Kung Pao Chicken', 'description': 'Spicy stir-fried chicken with peanuts', 'price': 15.99, 'vegetarian': False},
                    {'name': 'Sweet and Sour Pork', 'description': 'Crispy pork in tangy sweet sauce', 'price': 14.99, 'vegetarian': False},
                ]}
            ],
            'Indian': [
                {'category': 'Starters', 'items': [
                    {'name': 'Samosa', 'description': 'Crispy pastry filled with spiced potatoes', 'price': 5.99, 'vegetarian': True},
                    {'name': 'Chicken Tikka', 'description': 'Marinated grilled chicken', 'price': 11.99, 'vegetarian': False},
                ]},
                {'category': 'Main Course', 'items': [
                    {'name': 'Butter Chicken', 'description': 'Creamy tomato-based curry with tender chicken', 'price': 14.99, 'vegetarian': False},
                    {'name': 'Palak Paneer', 'description': 'Spinach curry with cottage cheese', 'price': 12.99, 'vegetarian': True},
                ]}
            ],
            'Mexican': [
                {'category': 'Tacos', 'items': [
                    {'name': 'Carne Asada Taco', 'description': 'Grilled steak with fresh salsa', 'price': 3.99, 'vegetarian': False},
                    {'name': 'Fish Taco', 'description': 'Battered fish with cabbage slaw', 'price': 4.99, 'vegetarian': False},
                ]},
                {'category': 'Burritos', 'items': [
                    {'name': 'Chicken Burrito', 'description': 'Large flour tortilla with chicken, rice, and beans', 'price': 9.99, 'vegetarian': False},
                    {'name': 'Veggie Burrito', 'description': 'Flour tortilla with vegetables and beans', 'price': 8.99, 'vegetarian': True},
                ]}
            ],
            'American': [
                {'category': 'Burgers', 'items': [
                    {'name': 'Classic Cheeseburger', 'description': 'Beef patty with cheese, lettuce, and tomato', 'price': 11.99, 'vegetarian': False},
                    {'name': 'Bacon Burger', 'description': 'Beef patty with crispy bacon and cheese', 'price': 13.99, 'vegetarian': False},
                ]},
                {'category': 'Sides', 'items': [
                    {'name': 'French Fries', 'description': 'Crispy golden fries', 'price': 4.99, 'vegetarian': True},
                    {'name': 'Onion Rings', 'description': 'Battered and fried onion rings', 'price': 5.99, 'vegetarian': True},
                ]}
            ],
            'Japanese': [
                {'category': 'Sushi', 'items': [
                    {'name': 'California Roll', 'description': 'Crab, avocado, and cucumber roll', 'price': 8.99, 'vegetarian': False},
                    {'name': 'Spicy Tuna Roll', 'description': 'Tuna with spicy mayo', 'price': 10.99, 'vegetarian': False},
                ]},
                {'category': 'Hot Dishes', 'items': [
                    {'name': 'Chicken Teriyaki', 'description': 'Grilled chicken with teriyaki sauce', 'price': 14.99, 'vegetarian': False},
                    {'name': 'Vegetable Tempura', 'description': 'Battered and fried vegetables', 'price': 11.99, 'vegetarian': True},
                ]}
            ]
        }
        
        # Get restaurant cuisine
        restaurant_cuisine = restaurant.cuisine.first()
        if not restaurant_cuisine:
            return
        
        cuisine_name = restaurant_cuisine.name
        if cuisine_name not in menu_templates:
            return
        
        template = menu_templates[cuisine_name]
        
        for category_data in template:
            category, created = Category.objects.get_or_create(
                restaurant=restaurant,
                name=category_data['category'],
                defaults={'order': len(Category.objects.filter(restaurant=restaurant))}
            )
            
            for item_data in category_data['items']:
                MenuItem.objects.get_or_create(
                    restaurant=restaurant,
                    category=category,
                    name=item_data['name'],
                    defaults={
                        'description': item_data['description'],
                        'price': Decimal(str(item_data['price'])),
                        'is_vegetarian': item_data['vegetarian'],
                        'is_available': True,
                        'preparation_time': 15,
                        'order': len(MenuItem.objects.filter(category=category))
                    }
                )