import sqlite3
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, transaction

from dishes.models import Dish, DishIngredient, Ingredient
from events.models import Event, EventDish, Organizer


class Command(BaseCommand):
    help = "Перенос данных из SQLite ПР7 в таблицы Django ORM."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source", type=Path,
            default=settings.BASE_DIR / "data" / "menu.sqlite",
        )

    def handle(self, *args, **options):
        uri = options["source"].resolve().as_uri() + "?mode=ro"
        try:
            with closing(sqlite3.connect(uri, uri=True)) as source:
                source.row_factory = sqlite3.Row
                source.execute("BEGIN")
                with transaction.atomic():
                    self.import_rows(source)
        except (sqlite3.Error, DatabaseError, ValueError) as error:
            raise CommandError(f"Перенос прерван: {error}") from error
        self.stdout.write(self.style.SUCCESS("Данные ПР7 перенесены."))

    def import_rows(self, source):
        for table, model in (
            ("users", Organizer), ("ingredients", Ingredient),
            ("dishes", Dish), ("events", Event),
        ):
            for row in source.execute(f"SELECT * FROM {table}"):
                fields = dict(row)
                pk = fields.pop("id")
                _, created = model.objects.get_or_create(
                    pk=pk, defaults=fields
                )
                if not created and not model.objects.filter(
                    pk=pk, **fields
                ).exists():
                    raise ValueError(f"Конфликт {table}, id={pk}")

        for row in source.execute("SELECT * FROM dish_ingredients"):
            serving, _ = DishIngredient.objects.get_or_create(
                dish_id=row["dish_id"], ingredient_id=row["ingredient_id"],
                defaults={"grams_for_guest": row["grams_for_guest"]},
            )
            if serving.grams_for_guest != row["grams_for_guest"]:
                raise ValueError(f"Конфликт нормы: {dict(row)}")
        for row in source.execute("SELECT * FROM event_dishes"):
            EventDish.objects.get_or_create(
                event_id=row["event_id"], dish_id=row["dish_id"]
            )
