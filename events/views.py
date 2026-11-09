from datetime import date

from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Prefetch, Q, Sum
from django.shortcuts import render

from dishes.models import Dish, DishIngredient
from events.models import Event, Organizer
from menu_planning.calculations import get_total_ingredients
from menu_planning.models import Dish as Recipe
from menu_planning.models import Ingredient


EVENT_SORTS = {
    "date": ("event_date", "id"),
    "guests": ("-guests", "event_date", "id"),
    "organizer": ("user__name", "event_date", "id"),
}


def events(request):
    value = request.GET.get("date", "")
    minimum = request.GET.get("min_guests", "0")
    term = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "date")
    status = request.GET.get("status", "")
    dish_id = request.GET.get("dish", "")
    organizer_id = request.GET.get("organizer", "")
    page_obj = None
    error = ""
    try:
        minimum = int(minimum or "0")
        page = int(request.GET.get("page", "1"))
        if not 0 <= minimum <= 1000000 or not 1 <= page <= 1000000:
            raise ValueError
        if status and status not in Event.Status.values:
            raise ValueError
        if any(
            value and not 1 <= int(value) <= 2**63 - 1
            for value in (dish_id, organizer_id)
        ):
            raise ValueError
        items = Event.objects.with_organizer().annotate(
            menu_count=Count("menu", distinct=True)
        )
        if value:
            value = date.fromisoformat(value).isoformat()
            items = items.on_date(value).filter(guests__gte=minimum)
        elif minimum:
            items = items.filter(guests__gte=minimum)
        if status:
            items = items.filter(status=status)
        if dish_id:
            items = items.filter(menu__pk=int(dish_id))
        if organizer_id:
            items = items.filter(user_id=int(organizer_id))
        if term:
            items = items.filter(
                Q(name__icontains=term) | Q(user__name__icontains=term)
            )
        ordered = items.order_by(*EVENT_SORTS.get(sort, EVENT_SORTS["date"]))
        page_obj = Paginator(ordered, 10).get_page(page)
    except ValueError:
        error = "Проверьте параметры фильтрации и номер страницы."
    return render(request, "events/event_list.html", {
        "events": page_obj, "selected_date": value, "min_guests": minimum,
        "error": error, "q": term, "sort": sort, "page_obj": page_obj,
        "status": status, "statuses": Event.Status.choices,
        "dish_id": dish_id, "organizer_id": organizer_id,
        "dish_options": Dish.objects.order_by("name").values_list(
            "pk", "name"
        ),
        "organizers": Organizer.objects.order_by("name").values_list(
            "pk", "name"
        ),
    }, status=400 if error else 200)


def event_detail(request, event_id: int):
    servings = DishIngredient.objects.select_related("ingredient").order_by(
        "ingredient_id"
    )
    dishes = Dish.objects.order_by("id").prefetch_related(
        Prefetch("servings", queryset=servings)
    )
    try:
        event = Event.objects.with_organizer().prefetch_related(
            Prefetch("menu", queryset=dishes)
        ).get(pk=event_id)
    except Event.DoesNotExist:
        return render(
            request, "events/event_detail.html", {"event": None}, status=404
        )
    menu = []
    for dish in event.menu.all():
        recipe = Recipe(dish.name, dish.dish_type, [
            Ingredient(row.ingredient.name, row.grams_for_guest)
            for row in dish.servings.all()
        ])
        menu.append({
            "dish": dish,
            "ingredients": get_total_ingredients(recipe, event.guests),
        })
    return render(request, "events/event_detail.html", {
        "event": event, "menu": menu, "menu_count": len(menu),
    })


def statistics(request):
    popularity = Dish.objects.values("id", "name").annotate(
        total=Count("events")
    ).order_by("-total", "id")
    return render(request, "events/statistics.html", {
        "dish_totals": Dish.objects.aggregate(
            total=Count("id"), types=Count("dish_type", distinct=True)
        ),
        "event_totals": Event.objects.aggregate(
            total=Count("id"), guest_total=Sum("guests", default=0),
            minimum=Min("guests", default=0), maximum=Max("guests", default=0),
            average=Avg("guests", default=0),
            active=Count("pk", filter=Q(status=Event.Status.ACTIVE)),
            cancelled=Count("pk", filter=Q(status=Event.Status.CANCELLED)),
            completed=Count("pk", filter=Q(status=Event.Status.COMPLETED)),
        ),
        "categories": Dish.objects.values("dish_type").annotate(
            total=Count("id")
        ).order_by("-total", "dish_type"),
        "popularity": popularity,
        "frequent": popularity.filter(total__gte=2),
    })
