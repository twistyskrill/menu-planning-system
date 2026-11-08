from django.core.validators import MinValueValidator
from django.db import models


class Organizer(models.Model):
    name = models.CharField("имя", max_length=200)
    email = models.EmailField("электронная почта", unique=True)

    class Meta:
        verbose_name = "организатор"
        verbose_name_plural = "организаторы"

    def __str__(self):
        return self.name


class EventQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Event.Status.ACTIVE)

    def on_date(self, value):
        return self.filter(event_date=value)

    def with_organizer(self):
        return self.select_related("user")


class Event(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Запланировано"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

    name = models.CharField("название", max_length=200)
    event_date = models.DateField("дата события", db_index=True)
    guests = models.PositiveIntegerField(
        "число гостей", validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        "статус", max_length=9, choices=Status.choices, default=Status.ACTIVE
    )

    objects = EventQuerySet.as_manager()
    user = models.ForeignKey(
        Organizer, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="events", verbose_name="организатор",
    )
    menu = models.ManyToManyField(
        "dishes.Dish", through="EventDish", related_name="events", blank=True,
        verbose_name="меню",
    )

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(guests__gt=0), name="event_positive_guests"
            ),
            models.CheckConstraint(
                condition=models.Q(
                    status__in=("active", "cancelled", "completed")
                ),
                name="event_valid_status",
            ),
        ]

    def __str__(self):
        return self.name


class EventDish(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="menu_entries",
        verbose_name="событие",
    )
    dish = models.ForeignKey(
        "dishes.Dish", on_delete=models.PROTECT, related_name="menu_entries",
        verbose_name="блюдо",
    )

    class Meta:
        verbose_name = "позиция меню"
        verbose_name_plural = "позиции меню"
        constraints = [models.UniqueConstraint(
            fields=["event", "dish"], name="unique_event_dish"
        )]

    def __str__(self):
        return f"{self.event}: {self.dish}"
