from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from dishes.models import Dish
from events.models import Event


def test_only_planned_events_exclude_dishes(seeded_orm):
    client = Client()
    event = Event.objects.get(pk=1)
    url = "/dishes/available/?date=2026-09-20"
    dish = Dish.objects.get(pk=1)
    assert dish.name not in client.get(url).content.decode()
    for status in (Event.Status.CANCELLED, Event.Status.COMPLETED):
        event.status = status
        event.save(update_fields=["status"])
        assert dish.name in client.get(url).content.decode()
    assert client.get(dish.get_absolute_url()).status_code == 200
    assert client.get("/dishes/slug/missing/").status_code == 404


def test_combined_event_filters_and_status_statistics(seeded_orm):
    event = Event.objects.get(pk=1)
    event.status = Event.Status.COMPLETED
    event.save(update_fields=["status"])
    client = Client()
    result = client.get("/events/", {
        "status": "completed", "dish": 1, "organizer": event.user_id,
        "date": event.event_date.isoformat(), "sort": "guests",
    })
    assert result.status_code == 200
    assert event.name in result.content.decode()
    assert "Новый год" not in result.content.decode()
    assert client.get("/events/?status=invalid").status_code == 400
    assert client.get("/events/?dish=oops").status_code == 400
    content = client.get("/events/statistics/").content.decode()
    assert "Запланировано: 2 · Отменено: 0 · Завершено: 1" in content


def test_admin_search_filters_and_related_cards(seeded_orm):
    user = get_user_model().objects.create_superuser(username="admin-test")
    client = Client()
    changelist = reverse("admin:events_event_changelist")
    assert client.get(changelist).status_code == 302
    client.force_login(user)
    result = client.get(changelist, {
        "q": "Овощной салат", "status__exact": "active",
    })
    content = result.content.decode()
    assert result.status_code == 200
    assert "День рождения" in content and "Новый год" not in content
    for url in (
        reverse("admin:dishes_dish_change", args=[1]),
        reverse("admin:events_organizer_change", args=[1]),
    ):
        result = client.get(url)
        assert result.status_code == 200
        assert "День рождения" in result.content.decode()
