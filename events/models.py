from django.core.validators import MinValueValidator
from django.db import models


class Organizer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    event_date = models.DateField(db_index=True)
    guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(
        Organizer, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="events",
    )
    menu = models.ManyToManyField(
        "dishes.Dish", through="EventDish", related_name="events", blank=True
    )

    class Meta:
        constraints = [models.CheckConstraint(
            condition=models.Q(guests__gt=0), name="event_positive_guests"
        )]

    def __str__(self):
        return self.name


class EventDish(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="menu_entries"
    )
    dish = models.ForeignKey(
        "dishes.Dish", on_delete=models.PROTECT, related_name="menu_entries"
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["event", "dish"], name="unique_event_dish"
        )]

    def __str__(self):
        return f"{self.event}: {self.dish}"
