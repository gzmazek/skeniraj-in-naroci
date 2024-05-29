CREATE TABLE User (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    name VARCHAR(150),
    password VARCHAR(128) NOT NULL,
    gender VARCHAR(10)
);

CREATE TABLE restaurant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    owner_id INTEGER REFERENCES User(id) ON DELETE SET NULL
);

CREATE TABLE table (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurant(id) ON DELETE CASCADE
);

CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value NUMERIC(10, 2) NOT NULL,
    allergen VARCHAR(255)
);

CREATE TABLE menu_item (
    table_id INTEGER REFERENCES table(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES item(id) ON DELETE CASCADE,
    PRIMARY KEY (table_id, item_id)
);

CREATE TABLE order (
    id SERIAL PRIMARY KEY,
    status VARCHAR(100) NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    table_id INTEGER REFERENCES table(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES User(id) ON DELETE SET NULL
);

CREATE TABLE order_item (
    order_id INTEGER REFERENCES order(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES item(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, item_id)
);
