from django.urls import path

from dishes import views


urlpatterns = [
    path("", views.dishes, name="dishes"),
    path("<int:dish_id>/", views.dish_detail, name="dish_detail"),
]
