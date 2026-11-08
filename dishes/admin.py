from django.contrib import admin

from dishes.models import Dish, DishIngredient, Ingredient


class ServingInline(admin.TabularInline):
    model = DishIngredient
    extra = 0


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type")
    list_filter = ("dish_type",)
    search_fields = ("name",)
    inlines = (ServingInline,)


admin.site.register(Ingredient)
