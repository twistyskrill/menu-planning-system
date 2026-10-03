import os

import pytest


django = pytest.importorskip("django")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_project.settings")
django.setup()

from django.test import Client  # noqa: E402


client = Client()


@pytest.mark.parametrize("url", ["/", "/dishes/", "/events/"])
def test_main_pages_are_available(url: str) -> None:
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "bootstrap@5.3.3" in content
    assert 'name="viewport"' in content


def test_dish_detail_uses_json_data() -> None:
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
