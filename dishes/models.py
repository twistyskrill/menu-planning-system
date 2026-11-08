from django.core.validators import MinValueValidator
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    grams_for_guest = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [models.CheckConstraint(
            condition=models.Q(grams_for_guest__gt=0),
            name="ingredient_positive_grams",
        )]

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dish_type = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(
        Ingredient, through="DishIngredient", related_name="dishes", blank=True
    )

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="servings"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, related_name="servings"
    )
    grams_for_guest = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["dish", "ingredient"], name="unique_dish_ingredient"
            ),
            models.CheckConstraint(
                condition=models.Q(grams_for_guest__gt=0),
                name="serving_positive_grams",
            ),
        ]

    def __str__(self):
        return f"{self.dish}: {self.ingredient}"
