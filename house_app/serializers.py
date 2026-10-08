from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Property, PropertyImage, Review, UserProfile


# ---------- Auth ----------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role', 'preferred_language')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_role(self, value):
        if value == 'admin':
            raise serializers.ValidationError('Нельзя зарегистрироваться как администратор.')
        return value

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'phone_number', 'role', 'preferred_language']
        read_only_fields = ['role']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


# ---------- Property ----------

class PropertyListSerializer(serializers.ModelSerializer):
    """Короткая карточка для списка."""
    images = PropertyImageSerializer(many=True, read_only=True)
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'deal_type', 'property_type', 'property_type_display',
            'region', 'city', 'district',
            'price', 'currency', 'price_type',
            'area', 'rooms', 'floor', 'total_floors',
            'condition', 'condition_display',
            'from_owner', 'is_urgent', 'images', 'created_at',
        ]


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Полная информация об одном объекте (и для изменения)."""
    seller = UserProfileSerializer(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['is_approved', 'created_at']


# ---------- Review ----------

class ReviewListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Review
        fields = ['id', 'author', 'seller', 'rating', 'created_at']


class ReviewDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Review
        fields = ['id', 'author', 'seller', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']