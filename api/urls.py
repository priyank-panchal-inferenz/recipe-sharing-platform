from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"api/recipe-category", RecipeCategoryApi)
router.register(r"api/recipe", RecipeViewSet)


urlpatterns = [
    path("api/login/", UserAuthenticationAPI.as_view()),
    path("api/create-user/", SignUpApi.as_view()),
    path("api/search-recipe/", RecipeSearchApi.as_view()),
    path("api/ratings/<int:pk>/" , ReviewAndRatingListApi.as_view()),
    path("api/ratings/create/" , ReviewAndRatingCreateApi.as_view()),
]
urlpatterns += router.urls
