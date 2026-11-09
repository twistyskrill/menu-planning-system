from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


def default_dish_slug():
    return uuid4().hex


class Ingredient(models.Model):
    name = models.CharField("название", max_length=200, unique=True)
    grams_for_guest = models.PositiveIntegerField(
        "граммов на гостя", validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
        constraints = [models.CheckConstraint(
            condition=models.Q(grams_for_guest__gt=0),
            name="ingredient_positive_grams",
        )]

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField("название", max_length=200, unique=True)
    dish_type = models.CharField("тип блюда", max_length=100)
    slug = models.SlugField(
        "адрес", max_length=220, unique=True, allow_unicode=True,
        default=default_dish_slug,
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="DishIngredient", related_name="dishes",
        blank=True,
        verbose_name="ингредиенты",
    )

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "блюда"

    def get_absolute_url(self):
        return reverse("dishes:dish_by_slug", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="servings",
        verbose_name="блюдо",
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, related_name="servings",
        verbose_name="ингредиент",
    )
    grams_for_guest = models.PositiveIntegerField(
        "граммов на гостя", validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "строка состава"
        verbose_name_plural = "состав блюда"
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
