from .models import User, Address
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.hashers import make_password


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        phone_number = attrs.get("phone_number")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username already exists"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already exists"})

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"phone_number": "Phone number already exists"})

        return attrs

    def create(self, validated_data):
        # Hash password before saving
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 
                  'full_name', 'profile_picture', 'date_of_birth']
        read_only_fields = ['id', 'username', 'email', 'phone_number']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # If this is set as default, remove default from other addresses
        if validated_data.get('is_default'):
            Address.objects.filter(user=validated_data['user'], is_default=True).update(is_default=False)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # If this is set as default, remove default from other addresses
        if validated_data.get('is_default'):
            Address.objects.filter(user=instance.user, is_default=True).exclude(id=instance.id).update(is_default=False)
        return super().update(instance, validated_data)
