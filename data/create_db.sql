CREATE TABLE AppUser (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    name VARCHAR(150),
    password VARCHAR(128) NOT NULL,
    gender VARCHAR(10)
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
    allergen VARCHAR(255)
);

CREATE TABLE MenuItem (
    dining_table_id INTEGER REFERENCES DiningTable(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES Item(id) ON DELETE CASCADE,
    PRIMARY KEY (dining_table_id, item_id)
);

CREATE TABLE CustomerOrder (
    id SERIAL PRIMARY KEY,
    status VARCHAR(100) NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    table_id INTEGER REFERENCES DiningTable(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES AppUser(id) ON DELETE SET NULL
);

CREATE TABLE OrderItem (
    customer_order_id INTEGER REFERENCES CustomerOrder(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES Item(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (customer_order_id, item_id)
);
