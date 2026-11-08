from django.contrib import admin

from events.models import Event, EventDish, Organizer


class MenuEntryInline(admin.TabularInline):
    model = EventDish
    autocomplete_fields = ("dish",)
    extra = 0


class OrganizerEventInline(admin.TabularInline):
    model = Event
    fields = ("name", "event_date", "status", "guests")
    show_change_link = True
    extra = 0
    can_delete = False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_date", "status", "guests", "user")
    list_select_related = ("user",)
    list_filter = (
        "status", "event_date", ("user", admin.RelatedOnlyFieldListFilter)
    )
    search_fields = ("name", "user__name", "user__email", "menu__name")
    ordering = ("-event_date", "pk")
    autocomplete_fields = ("user",)
    date_hierarchy = "event_date"
    inlines = (MenuEntryInline,)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")
    ordering = ("name", "pk")
    inlines = (OrganizerEventInline,)


admin.site.site_header = "Управление праздничным меню"
admin.site.site_title = "Праздничное меню"
admin.site.index_title = "Данные проекта"
