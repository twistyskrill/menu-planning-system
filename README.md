# Система планирования праздничного меню

Учебное приложение для планирования событий, праздничных меню и количества
ингредиентов. Консольная версия из ПР3 дополнена базовым веб-интерфейсом на
Django в рамках ПР5 и переведена на Django-шаблоны в ПР6.
В ПР7 веб-приложение получает данные из SQLite через стандартный `sqlite3`.

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

Изменение данных через веб-формы и перенос сущностей в Django ORM
отложены до следующих практических работ. JSON и консольный интерфейс ПР3
сохранены; веб-приложение читает отдельную базу `data/menu.sqlite`.

## Технологии

- Python 3;
- Django 5.2;
- HTML и Bootstrap 5.3;
- JSON;
- SQLite и стандартный модуль Python sqlite3;
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
| `/dishes/` | `dishes.views.dishes()` | каталог SQLite, поиск по `q` и `type` |
| `/dishes/<int:dish_id>/` | `dishes.views.dish_detail()` | карточка блюда и ингредиенты |
| `/events/` | `events.views.events()` | события SQLite, фильтры `date` и `min_guests` |
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

Создайте базу предметной области из JSON и проверьте проект:

```bash
python -m db.import_json
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
pytest -v
flake8 . --extend-exclude=.venv,venv,tmp,output
```

Тесты проверяют прежнюю предметную логику, загрузку JSON, доступность страниц,
динамические URL, расчёт ингредиентов и ответы 404. Проверки ПР7 охватывают
повторный импорт, откат транзакции при ошибке, внешние ключи, NULL,
параметризованный поиск, пагинацию, статистику и чтение изменений SQLite.

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

В ПР7 данные веб-приложения хранятся в SQLite. Формы создания и редактирования,
Django ORM, регистрация и авторизация относятся к следующим работам.

## ПР7 База данных и SQL

Основные файлы: `sql/schema.sql` создаёт таблицы и индексы;
`sql/queries.sql` содержит 12 именованных запросов; `db/database.py`
открывает соединения с `sqlite3.Row`, включает внешние ключи и закрывает
соединения; `db/import_json.py` переносит JSON; `db/repository.py`
преобразует результаты SQL в прежние классы предметной области.
Каталог SQL служит единственным источником запросов для веб-приложения.

| Таблица | Поля и ограничения |
| --- | --- |
| users | id INTEGER PK, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL |
| ingredients | id INTEGER PK, name TEXT UNIQUE NOT NULL, grams_for_guest INTEGER > 0 |
| dishes | id INTEGER PK, name TEXT UNIQUE NOT NULL, dish_type TEXT NOT NULL |
| events | id INTEGER PK, name TEXT NOT NULL, event_date TEXT ISO-дата, guests INTEGER > 0, user_id INTEGER FK NULL |
| dish_ingredients | dish_id FK, ingredient_id FK, grams_for_guest INTEGER > 0; составной PK |
| event_dishes | event_id FK, dish_id FK; составной PK |

Связи: пользователь 1:N события; события M:N блюда через event_dishes;
блюда M:N ингредиенты через dish_ingredients. Норма массы хранится в связи
с блюдом, что позволяет одному ингредиенту иметь разные нормы в рецептах.
Отсутствующий организатор задаётся NULL. При удалении пользователя
события сохраняются с NULL; при удалении события удаляются связи его меню.
Отдельная `db.sqlite3` предназначена для служебных приложений Django;
предметные таблицы не используют ORM и миграции.

Импорт: `python -m db.import_json`. Он **заменяет все данные SQL-базы**
снимком JSON в одной транзакции, поэтому повторный запуск не создаёт дублей.
Изменения, внесённые вручную в SQLite, будут заменены. Ошибка приводит
к rollback; исходные JSON не изменяются. Порядок: пользователи и ингредиенты,
блюда, события, состав рецептов, меню. Вставки выполняются executemany,
значения передаются через `?`, изменения сохраняются commit.
Результат импорта: 2 пользователя, 17 ингредиентов, 6 блюд, 3 события,
19 связей состава и 9 связей меню.

Для отдельной базы: `python -m db.import_json --database data/demo.sqlite`.
В тестах путь можно задать настройкой `MENU_DATABASE`. Сервер не импортирует
JSON автоматически: изменение SQLite сразу видно при обновлении страницы,
изменение JSON влияет на веб только после явного импорта.

| Запрос в queries.sql | Использование |
| --- | --- |
| dishes, events | два списка объектов, страницы каталога и событий |
| dish_search, event_search | WHERE, формы поиска в каталогах |
| composition, menus | JOIN, состав блюд и меню в карточках |
| dish_totals, event_totals | COUNT, SUM, MIN, MAX, AVG на странице статистики |
| categories, popularity | GROUP BY, категории и число событий для каждого блюда, включая нулевое |
| frequent | HAVING, блюда как минимум в двух событиях |
| available | NOT IN, JOIN, WHERE, ORDER BY, LIMIT и OFFSET для подбора по дате |

Примеры: `/dishes/?type=десерт`, `/dishes/?q=салат`,
`/events/?date=2026-12-31&min_guests=6`,
`/dishes/available/?date=2026-09-20`.
Поиск названия учитывает регистр Unicode. Неверная дата или число гостей
дают HTTP 400 с пояснением. Пустая выборка показывает сообщение.
Подбор исключает блюда из всех событий на дату: это аналог поиска свободных
помещений из методички, адаптированный к разнообразию меню; ограничений
на повторное приготовление блюд система не устанавливает.

Проверка SQL в SQLite CLI: `sqlite3 data/menu.sqlite`, затем `.read sql/schema.sql`.
Для запросов с `?` задайте `.parameter init` и `.parameter set ?1 значение`
(и остальные параметры по порядку), затем выполните нужный запрос.
В среде без отдельного sqlite3 CLI доступен CLI Python 3.12+:
`python -m sqlite3 data/menu.sqlite "SELECT COUNT(*) FROM dishes;"`.
Для проверки структуры: `PRAGMA table_info(events);`,
`PRAGMA foreign_key_list(event_dishes);`, `PRAGMA foreign_key_check;`.

Архитектура ПР7: SQLite → SQL → sqlite3.Row → предметные объекты / context
→ Django templates → браузер. Прежний путь JSON → storage → классы
→ консольный интерфейс сохранён для сравнения.
