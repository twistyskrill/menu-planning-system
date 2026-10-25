-- name: dishes
-- 1. SELECT: каталог блюд с устойчивым порядком.
SELECT id, name, dish_type FROM dishes ORDER BY id;

-- name: events
-- 2. SELECT и JOIN: события и необязательный организатор.
SELECT e.*, u.name AS user_name, u.email
FROM events AS e LEFT JOIN users AS u ON u.id = e.user_id
ORDER BY e.event_date, e.id;

-- name: dish_search
-- 3. WHERE: поиск по названию и типу; значения передаются параметрами.
SELECT id, name, dish_type FROM dishes
WHERE (? = '' OR instr(name, ?) > 0)
  AND (? = '' OR dish_type = ?)
ORDER BY id;

-- name: event_search
-- 4. WHERE и JOIN: события по дате и минимальному числу гостей.
SELECT e.*, u.name AS user_name, u.email
FROM events AS e LEFT JOIN users AS u ON u.id = e.user_id
WHERE (? = '' OR e.event_date = ?) AND e.guests >= ?
ORDER BY e.event_date, e.id;

-- name: composition
-- 5. JOIN: состав блюд и норма на гостя.
SELECT di.dish_id, i.name, di.grams_for_guest
FROM dish_ingredients AS di JOIN ingredients AS i ON i.id = di.ingredient_id
ORDER BY di.dish_id, i.id;

-- name: menus
-- 6. JOIN: блюда в меню событий.
SELECT ed.event_id, d.id AS dish_id, d.name, d.dish_type
FROM event_dishes AS ed JOIN dishes AS d ON d.id = ed.dish_id
ORDER BY ed.event_id, d.id;

-- name: dish_totals
-- 7. Агрегатные функции: размер каталога и число типов.
SELECT COUNT(*) AS total, COUNT(DISTINCT dish_type) AS types FROM dishes;

-- name: event_totals
-- 8. Агрегатные функции: гости и события; пустая база даёт нули.
SELECT COUNT(*) AS total, COALESCE(SUM(guests), 0) AS guests,
       COALESCE(MIN(guests), 0) AS minimum,
       COALESCE(MAX(guests), 0) AS maximum,
       COALESCE(AVG(guests), 0) AS average FROM events;

-- name: categories
-- 9. GROUP BY: число блюд по типам.
SELECT dish_type, COUNT(*) AS total FROM dishes
GROUP BY dish_type ORDER BY total DESC, dish_type;

-- name: popularity
-- 10. GROUP BY и LEFT JOIN: популярность, включая неиспользованные блюда.
SELECT d.id, d.name, COUNT(ed.event_id) AS total
FROM dishes AS d LEFT JOIN event_dishes AS ed ON ed.dish_id = d.id
GROUP BY d.id, d.name ORDER BY total DESC, d.id;

-- name: frequent
-- 11. HAVING: блюда, включённые как минимум в два события.
SELECT d.id, d.name, COUNT(ed.event_id) AS total
FROM dishes AS d JOIN event_dishes AS ed ON ed.dish_id = d.id
GROUP BY d.id, d.name HAVING COUNT(ed.event_id) >= ?
ORDER BY total DESC, d.id;

-- name: available
-- 12. Подзапрос: блюда, ещё не включённые в меню на выбранную дату.
SELECT id, name, dish_type FROM dishes
WHERE id NOT IN (
    SELECT ed.dish_id FROM event_dishes AS ed
    JOIN events AS e ON e.id = ed.event_id WHERE e.event_date = ?
)
ORDER BY id LIMIT ? OFFSET ?;
