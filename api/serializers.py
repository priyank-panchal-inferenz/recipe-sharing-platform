from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Recipe, RecipeCategory, ReviewAndRating
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = User.objects.create(**validated_data)
        return user


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeSerachSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    user = serializers.CharField(source="user.first_name")

    class Meta:
        model = Recipe
        fields = "__all__"


class ReviewAndRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAndRating
        fields = "__all__"


class ReviewAndRatingAddSerializer(ReviewAndRatingSerializer):
    user = serializers.CharField(source="user.first_name", read_only=True)
