from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    RecipeCategorySerializer,
    RecipeSerializer,
    RecipeSerachSerializer,
    ReviewAndRatingSerializer,
    ReviewAndRatingAddSerializer,
)
from rest_framework import status, viewsets, permissions
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, mixins, generics
from django.db.models import Avg


class UserAuthenticationAPI(ObtainAuthToken):
    """
    User Authentication API check user is valid or not.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "token": token.key,
                "user_id": user.pk,
                "email": user.username,
            }
        )


class SignUpApi(APIView):
    """
    Sign up user api create new user.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeCategoryApi(viewsets.ModelViewSet):
    """Recipe cateogry this is not user based all of can show categories"""

    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ListWithoutAuthentication(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow access to the list() method without requiring authentication
        return request.method in ["GET"]


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Recipe crud operations based on user.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeSearchApi(generics.ListAPIView, mixins.ListModelMixin):
    """
    Recipe Search api using ?search= paramters we can filter from title category name
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerachSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "category__name", "cooking_time"]


class ReviewAndRatingListApi(generics.RetrieveAPIView):
    """
    Get Review and Rating with avg rating.
    """

    queryset = ReviewAndRating.objects.all()
    serializer_class = ReviewAndRatingSerializer

    def retrieve(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get("pk")
        average_rating = ReviewAndRating.objects.filter(recipe_id=recipe_id).aggregate(
            avg_rating=Avg("rating_number")
        )["avg_rating"]
        queryset = ReviewAndRating.objects.filter(recipe_id=recipe_id)
        serializer = self.get_serializer(queryset, many=True)
        data = {"average_rating": average_rating, "reviews": serializer.data}
        return Response(data)


class ReviewAndRatingCreateApi(generics.CreateAPIView):
    """
    Review and Rating Create API.
    """

    serializer_class = ReviewAndRatingAddSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        recipe = self.request.data.get("recipe")
        try:
            recipe = Recipe.objects.get(id=recipe)
            serializer.save(user=self.request.user, recipe=recipe)
        except Recipe.DoesNotExist:
            return Response(
                {"message": "Recipe not found."}, status=status.HTTP_400_BAD_REQUEST
            )
