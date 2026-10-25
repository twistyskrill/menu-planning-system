from django.urls import path

from dishes import views


app_name = "dishes"


urlpatterns = [
    path("", views.dishes, name="dishes"),
    path("available/", views.available, name="available"),
    path("<int:dish_id>/", views.dish_detail, name="dish_detail"),
]
