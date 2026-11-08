# Система планирования праздничного меню

Учебное приложение для планирования событий, праздничных меню и количества
ингредиентов. Консольная версия из ПР3 дополнена базовым веб-интерфейсом на
Django в рамках ПР5 и переведена на Django-шаблоны в ПР6.
В ПР9 веб-приложение работает с SQLite через Django ORM.

## Возможности

- просмотр списка блюд и карточки отдельного блюда;
- просмотр списка событий и карточки отдельного события;
- отображение пользователя, меню и количества гостей события;
- расчёт необходимого количества каждого ингредиента для всех гостей;
- навигация между главной страницей, блюдами и событиями;
- обработка неизвестных идентификаторов с HTTP-кодом 404;
- работа прежней консольной версии с чтением и записью JSON.
- поиск блюд по названию и типу, событий по дате и числу гостей;
- подбор блюд, ещё не включённых в меню на выбранную дату;
- статистика гостей, категорий и использования блюд.

Редактирование данных доступно в Django Admin. Консольная версия
по-прежнему работает с JSON. Исходная база ПР7 хранится в `data/menu.sqlite`
и используется для переноса записей в локальную `db.sqlite3`.

## Технологии

- Python 3;
- Django 5.2;
- HTML и Bootstrap 5.3;
- JSON;
- SQLite и Django ORM;
- pytest;
- flake8.

## Предметная область

Основные объекты проекта:

- `Ingredient` — ингредиент и его масса на одного гостя;
- `Dish` — блюдо, тип блюда и список ингредиентов;
- `User` — пользователь, планирующий меню;
- `Event` — событие с датой, числом гостей, пользователем и меню.

Объект `Event` связан с `User` и содержит объекты `Dish`. Каждый объект `Dish`
содержит объекты `Ingredient`. При открытии карточки события приложение использует
логику ПР3 и рассчитывает массу ингредиентов с учётом количества гостей.

## Веб-страницы

| URL | View-функция | Назначение |
| --- | --- | --- |
| `/` | `homepage.views.index()` | описание проекта и навигация |
| `/dishes/` | `dishes.views.dishes()` | поиск по `q`, `type` и `ingredient`, сортировка `sort` |
| `/dishes/<int:dish_id>/` | `dishes.views.dish_detail()` | карточка блюда и ингредиенты |
| `/events/` | `events.views.events()` | фильтры `date` и `min_guests`, поиск `q`, сортировка `sort`, пагинация |
| `/dishes/available/` | `dishes.views.available()` | подбор по `date`, страницы `page` |
| `/events/statistics/` | `events.views.statistics()` | итоги, категории, популярность |
| `/events/<int:event_id>/` | `events.views.event_detail()` | событие, пользователь, меню и расчёты |

Например, `/dishes/1/` и `/events/1/` открывают существующие объекты, а
`/dishes/999/` и `/events/999/` возвращают страницу «не найдено» и HTTP 404.

Для неизвестных адресов настроен общий `handler404`, вызывающий
`homepage.views.page_not_found()` и шаблон `templates/404.html`. Страница использует общий HTML-каркас,
Bootstrap и кнопку возврата на главную. Для проверки установите `DEBUG = False`
в `menu_project/settings.py` и откройте `/nonexistent/` или `/dishes/abc/`.
После проверки верните `DEBUG = True`: в режиме отладки Django показывает
техническую страницу 404 вместо пользовательского обработчика.

## Структура проекта

```text
menu-planning-system/
├── manage.py
├── main.py
├── requirements.txt
├── menu_project/          # конфигурация Django-проекта
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/            # base.html, 404.html, includes/navigation.html
├── homepage/              # главная страница, CSS, JavaScript и логотип
│   ├── urls.py
│   └── views.py
├── dishes/                # список и карточки блюд
│   ├── urls.py
│   └── views.py
├── events/                # список и карточки событий
│   ├── urls.py
│   └── views.py
├── menu_planning/         # объектная модель и логика ПР3
│   ├── models.py
│   ├── calculations.py
│   ├── dishes.py
│   ├── events.py
│   ├── users.py
│   ├── storage.py
│   └── utils.py
├── data/                  # JSON-хранилище
│   ├── events.json
│   ├── dishes.json
│   ├── ingredients.json
│   └── users.json
└── tests/                 # тесты предметной логики и веб-страниц
```

Маршруты распределены по двум уровням: `menu_project/urls.py` подключает
маршруты приложений, а каждое приложение описывает собственные адреса в своём
`urls.py`. Приложения зарегистрированы в `INSTALLED_APPS`; язык — русский,
часовой пояс — `Europe/Moscow`.

Приложение пользователей отдельно не создаётся: класс `User` ПР3 остаётся частью
консольной предметной модели, а для будущей веб-аутентификации Django уже содержит
`django.contrib.auth`.

## Запуск веб-версии

Создайте и активируйте виртуальное окружение, затем установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

На Windows команда активации: `.venv\Scripts\activate`.

Примените миграции и перенесите данные из исходной базы ПР7:

```bash
python manage.py migrate
python manage.py import_pr7
python manage.py check
python manage.py runserver
```

После запуска откройте <http://127.0.0.1:8000/>.

## Консольная версия

Консольный интерфейс ПР3 сохранён и запускается отдельно:

```bash
python main.py
```

## Проверка

```bash
python manage.py check
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
pytest -v
flake8 . --extend-exclude=.venv,venv,tmp,output,migrations
```

Тесты Django используют отдельную временную базу. Они проверяют перенос
данных, обратные связи, сохранение расчётов и маршрутов, фильтры,
пагинацию, статистику и пустые результаты. Отдельные тесты проверяют
консольную логику и архивный импорт ПР7.

## Текущее состояние и дальнейшее развитие

В ПР5 реализованы Django-проект, приложения `homepage`, `dishes` и `events`,
двухуровневая маршрутизация, view-функции, HTML-страницы, Bootstrap-навигация и
отображение данных предметной области из JSON.

В ПР6 все веб-представления используют `render()` и передают данные через
контекст. HTML вынесен в Django Template Language; функция `page()` удалена.
Общий `templates/base.html` задаёт блоки `title` и `content`, Bootstrap,
подвал и статику. Дочерние страницы используют `extends`, а навигация,
карточки блюд и статус меню подключаются через `include`.

Шаблоны приложений:
- `homepage/templates/homepage/index.html`;
- `dishes/templates/dishes/dish_list.html` и `dish_detail.html`;
- `dishes/templates/dishes/includes/dish_card.html`;
- `events/templates/events/event_list.html` и `event_detail.html`;
- `events/templates/events/includes/event_status.html`.

Циклы `for` выводят коллекции, `empty` обрабатывает пустые списки, `if`
показывает отсутствие объекта и состояние меню. Статус «Меню составлено» /
«Меню не составлено» определяется существующим `Event.menu`: у нашей модели
нет отмены бронирования из примера Roomly. Модели и JSON-формат сохранены.
Расчёты ингредиентов выполняются в Python, а не в шаблонах.

В `urls.py` приложений настроены `app_name`; ссылки используют `{% url %}`
с пространствами имён `homepage`, `dishes`, `events` и прежними именами
маршрутов (`homepage:index`, `dishes:dishes`, `dishes:dish_detail`,
`events:events`, `events:event_detail`). Адреса страниц сохранены.

Фильтры `length`, `default` и `date` выводят количество элементов,
значения по умолчанию и дату в формате ДД.ММ.ГГГГ. ISO-даты из SQLite
преобразуются во view в `date` без изменения предметной модели.
Отсутствующий объект передаётся в шаблон как `None`, обрабатывается через
`if` / `else` и возвращается с HTTP 404.

Статические файлы находятся в `homepage/static/homepage/`:
`css/style.css` оформляет карточки, статусы и подвал, `img/logo.svg`
содержит логотип с тарелкой, `js/main.js` выводит текущий год в подвале.
Все ресурсы подключены через `{% load static %}` и `{% static %}`.
Проверка поиска: `python manage.py findstatic homepage/img/logo.svg`.

## ПР9 Модели и связи

| Модель | Поля и связи |
| --- | --- |
| `dishes.Ingredient` | уникальное имя, положительная масса на гостя |
| `dishes.Dish` | уникальное имя, тип, ингредиенты через `DishIngredient` |
| `dishes.DishIngredient` | блюдо, ингредиент, норма для конкретного блюда |
| `events.Organizer` | имя, уникальная почта |
| `events.Event` | название, дата, положительное число гостей, организатор, меню |
| `events.EventDish` | уникальная пара события и блюда |

Первичные ключи создаёт Django. При удалении организатора его события
сохраняются с пустым полем `user` (`SET_NULL`). При удалении события его
строки меню удаляются каскадно. `PROTECT` защищает ингредиенты в рецептах
и блюда, включённые в меню. Обратные связи доступны как `organizer.events`,
`dish.events` и `ingredient.dishes`.

Миграции `dishes/0001_initial` и `events/0001_initial` создают таблицы
в `db.sqlite3`. Команда `python manage.py import_pr7` читает
`data/menu.sqlite` в режиме только чтения и записывает данные через ORM
в одной транзакции. Она сохраняет ID и все связи. Повторный импорт того же
снимка не создаёт дублей. Конфликт с изменёнными данными откатывает перенос.
Другой снимок можно указать через `--source путь/к/menu.sqlite`.

SQL-схема, запросы и загрузчик JSON из ПР7 остаются в `sql/` и `db/`
для воспроизведения исходной базы. Сайт читает только таблицы Django.

### ORM в представлениях

| № | Выборка | Где используется |
| --- | --- | --- |
| 1 | `Dish.objects.all()` | каталог |
| 2 | `filter(dish_type=...)` | тип блюда |
| 3 | `StrIndex` и `filter(match__gt=0)` | поиск по части названия с учётом регистра |
| 4 | `filter(ingredients__name__icontains=...).distinct()` | поиск по связанному ингредиенту |
| 5 | `values("dish_type").distinct().order_by("dish_type")` | варианты фильтра |
| 6 | `filter(pk=...).first()` | карточка блюда |
| 7 | `servings.select_related("ingredient")` | состав блюда |
| 8 | `exclude(events__event_date=...)` | подбор блюд по дате |
| 9 | `select_related("user").annotate(menu_count=Count("menu"))` | список событий и статус меню |
| 10 | `filter(event_date=..., guests__gte=...)` | дата и число гостей |
| 11 | `filter(guests__gte=...)` | минимум гостей без даты |
| 12 | `filter(Q(name__icontains=...) \| Q(user__name__icontains=...))` | поиск по событию или организатору |
| 13 | `order_by(...)` с разрешёнными полями | сортировка по дате, гостям или организатору |
| 14 | `select_related("user").prefetch_related(...).get(pk=...)` | событие, меню и нормы |
| 15 | `Dish.objects.aggregate(...)` | число блюд и типов |
| 16 | `Event.objects.aggregate(Count, Sum, Min, Max, Avg)` | сводка по гостям |
| 17 | `values("dish_type").annotate(total=Count("id"))` | группировка блюд по типу |
| 18 | `values("id", "name").annotate(total=Count("events"))` | популярность, включая блюда без событий |
| 19 | `filter(total__gte=2)` | блюда в меню нескольких событий |

`Paginator` разбивает список событий и подбор блюд на страницы по 10 записей.
Ссылки сохраняют GET-параметры через тег `querystring`. Некорректный формат
даты, числа гостей или страницы даёт HTTP 400, отсутствующий объект — HTTP 404.
Номер за пределами результатов открывает последнюю страницу. Для
неизвестной сортировки используется порядок по умолчанию.

### CRUD и выгрузка

Запустите `python manage.py createsuperuser` и откройте `/admin/` для
создания, просмотра, изменения и удаления записей. Состав блюда и меню
редактируются в карточках блюда и события. Пример в `python manage.py shell`:

```python
from events.models import Event

event = Event.objects.create(name="Демонстрация", event_date="2026-12-20", guests=4)
event = Event.objects.get(pk=event.pk)
event.guests = 8
event.save(update_fields=["guests"])
event.refresh_from_db()
assert event.guests == 8
event.delete()
```

Выгрузка предметных данных: `python manage.py dumpdata dishes events --indent 2`.
