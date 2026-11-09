from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from dishes.models import Dish, DishIngredient, Ingredient
from events.models import EventDish


class ServingInline(admin.TabularInline):
    model = DishIngredient
    autocomplete_fields = ("ingredient",)
    extra = 0


class DishEventInline(admin.TabularInline):
    model = EventDish
    fields = ("event_link", "event_date", "event_status")
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("event")

    @admin.display(description="Событие")
    def event_link(self, obj):
        url = reverse("admin:events_event_change", args=[obj.event_id])
        return format_html('<a href="{}">{}</a>', url, obj.event)

    @admin.display(description="Дата")
    def event_date(self, obj):
        return obj.event.event_date

    @admin.display(description="Статус")
    def event_status(self, obj):
        return obj.event.get_status_display()


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "slug")
    list_filter = ("dish_type",)
    search_fields = ("name", "ingredients__name")
    ordering = ("name", "pk")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (ServingInline, DishEventInline)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "grams_for_guest")
    search_fields = ("name",)
    ordering = ("name", "pk")
