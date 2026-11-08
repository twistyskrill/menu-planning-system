import pytest

from dishes.models import Dish
from events.models import Event
from django.test import Client, override_settings


pytestmark = pytest.mark.usefixtures("seeded_orm")
client = Client()


@pytest.mark.parametrize("url", ["/", "/dishes/", "/events/"])
def test_main_pages_are_available(url: str) -> None:
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "bootstrap@5.3.3" in content
    assert 'name="viewport"' in content


def test_dish_detail_uses_project_data() -> None:
    response = client.get("/dishes/1/")

    assert response.status_code == 200
    assert "Овощной салат" in response.content.decode()


def test_event_detail_calculates_ingredients() -> None:
    response = client.get("/events/1/")
    content = response.content.decode()

    assert response.status_code == 200
    assert "День рождения" in content
    assert "огурец — 800 г" in content


@pytest.mark.parametrize("url", ["/dishes/999/", "/events/999/"])
def test_unknown_object_returns_404(url: str) -> None:
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize("url", ["/nonexistent/", "/dishes/abc/"])
def test_unknown_url_uses_custom_404_page(url: str) -> None:
    with override_settings(DEBUG=False):
        response = client.get(url)

    assert response.status_code == 404
    content = response.content.decode()
    assert "404 — страница не найдена" in content
    assert "bootstrap@5.3.3" in content
    assert '<a href="/" class="btn btn-primary">На главную</a>' in content


@pytest.mark.parametrize("url,model,message", [
    ("/dishes/", Dish, "Блюда не найдены."),
    ("/events/", Event, "События не найдены."),
])
def test_empty_lists(url, model, message):
    Event.objects.all().delete()
    model.objects.all().delete()
    response = client.get(url)
    assert response.status_code == 200
    assert message in response.content.decode()


def test_empty_menu_status_and_missing_user():
    event = Event.objects.create(
        name="Праздник", event_date="2026-10-17", guests=4
    )
    for url in ["/events/", f"/events/{event.pk}/"]:
        response = client.get(url)
        content = response.content.decode()
        assert response.status_code == 200
        assert "Меню не составлено" in content
        assert "не указан" in content
        assert "17.10.2026" in content
    assert "В меню пока нет блюд." in content


def test_templates_escape_dish_name():
    dish = Dish.objects.create(
        name="<script>alert(1)</script>", dish_type="салат"
    )
    for url in ["/dishes/", f"/dishes/{dish.pk}/"]:
        content = client.get(url).content.decode()
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in content
        assert "<script>alert(1)</script>" not in content


def test_named_routes_and_shared_static():
    from django.urls import reverse

    assert reverse("homepage:index") == "/"
    assert reverse("dishes:dishes") == "/dishes/"
    assert reverse("dishes:dish_detail", args=[1]) == "/dishes/1/"
    assert reverse("events:events") == "/events/"
    assert reverse("events:event_detail", args=[1]) == "/events/1/"
    for url in ["/", "/dishes/", "/events/", "/dishes/9999/",
                "/events/9999/"]:
        content = client.get(url).content.decode()
        for resource in ["css/style.css", "img/logo.svg", "js/main.js"]:
            assert "/static/homepage/" + resource in content
        assert 'id="current-year"' in content
    assert "Меню составлено" in client.get("/events/1/").content.decode()
