from django.contrib import admin

from events.models import Event, EventDish, Organizer


class MenuEntryInline(admin.TabularInline):
    model = EventDish
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_date", "guests", "user")
    list_select_related = ("user",)
    search_fields = ("name", "user__name")
    inlines = (MenuEntryInline,)


admin.site.register(Organizer)
