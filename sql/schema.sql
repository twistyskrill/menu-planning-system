PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    grams_for_guest INTEGER NOT NULL CHECK (grams_for_guest > 0)
);
CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    dish_type TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    event_date TEXT NOT NULL CHECK (date(event_date) IS NOT NULL),
    guests INTEGER NOT NULL CHECK (guests > 0),
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS dish_ingredients (
    dish_id INTEGER NOT NULL REFERENCES dishes(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(id),
    grams_for_guest INTEGER NOT NULL CHECK (grams_for_guest > 0),
    PRIMARY KEY (dish_id, ingredient_id)
);
CREATE TABLE IF NOT EXISTS event_dishes (
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    dish_id INTEGER NOT NULL REFERENCES dishes(id),
    PRIMARY KEY (event_id, dish_id)
);
CREATE INDEX IF NOT EXISTS events_date_idx ON events(event_date);
CREATE INDEX IF NOT EXISTS event_dishes_dish_idx ON event_dishes(dish_id);
