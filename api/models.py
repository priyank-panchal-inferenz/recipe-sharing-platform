from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    ingredients = models.TextField(null=True)
    preparation_steps = models.TextField(null=True)
    cooking_time = models.IntegerField(help_text="Cooking time", null=True)
    serving_size = models.IntegerField(help_text="Number of servings", null=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class ReviewAndRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_number = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review_text = models.TextField(null= True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
