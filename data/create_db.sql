CREATE TABLE AppUser (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Restaurant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    owner_id INTEGER REFERENCES AppUser(id) ON DELETE SET NULL
);

CREATE TABLE DiningTable (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES Restaurant(id) ON DELETE CASCADE
);

CREATE TABLE Item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value NUMERIC(10, 2) NOT NULL,
    tags BYTEA DEFAULT E'\\x00000000'
);

CREATE TABLE RestaurantMenu (
    restaurant_id INTEGER REFERENCES Restaurant(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES Item(id) ON DELETE CASCADE,
    PRIMARY KEY (restaurant_id, item_id)
);

CREATE TABLE CustomerOrder (
    id SERIAL PRIMARY KEY,
    status VARCHAR(100) NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    table_id INTEGER REFERENCES DiningTable(id) ON DELETE SET NULL,
    user_id INTEGER REFERENCES AppUser(id) ON DELETE SET NULL
);

CREATE TABLE OrderItem (
    customer_order_id INTEGER REFERENCES CustomerOrder(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES Item(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (customer_order_id, item_id)
);