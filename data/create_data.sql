DO $$
DECLARE
    existing_items INT;
BEGIN
    SELECT COUNT(*) INTO existing_items FROM Item WHERE name IN ('Espresso', 'Cappuccino', 'Latte', 'Croissant', 'Pancakes', 'Orange Juice', 'Scrambled Eggs', 'Club Sandwich', 'Caesar Salad', 'Grilled Cheese');
    IF existing_items = 0 THEN
        INSERT INTO Item (name, value, tags) VALUES 
        ('Espresso', 2.50, '\\x00000001'),
        ('Cappuccino', 3.50, '\\x00000001'),
        ('Latte', 4.00, '\\x00000001'),
        ('Croissant', 2.00, '\\x00000001'),
        ('Pancakes', 5.50, '\\x00000001'),
        ('Orange Juice', 3.00, '\\x00000001'),
        ('Scrambled Eggs', 6.00, '\\x00000001'),
        ('Club Sandwich', 7.50, '\\x00000001'),
        ('Caesar Salad', 8.50, '\\x00000001'),
        ('Grilled Cheese', 4.50, '\\x00000001');
    END IF;
END $$;

-- simulated user, can't be loged in
INSERT INTO AppUser (email, name, surname, password) VALUES
('john.doe@example.com', 'John', 'Doe', 'password123'),
('jane.smith@example.com', 'Jane', 'Smith', 'password123'),
('alice.jones@example.com', 'Alice', 'Jones', 'password123'),
('bob.brown@example.com', 'Bob', 'Brown', 'password123'),
('charlie.davis@example.com', 'Charlie', 'Davis', 'password123');

DO $$
DECLARE
    table_id INTEGER;
    user_id INTEGER;
    order_id INTEGER;
    order_date TIMESTAMP;
    menu_item_id INTEGER;
    item_quantity INTEGER;
    order_status VARCHAR(50);
    item_status VARCHAR(50);
    item_exists BOOLEAN;
BEGIN
    FOR i IN 1..9000 LOOP  -- Simulating 2 orders for testing (increase to 9000 for full simulation)
        SELECT id INTO table_id FROM DiningTable WHERE restaurant_id = (SELECT id FROM Restaurant WHERE name = 'Kavarna Rog') ORDER BY RANDOM() LIMIT 1;
        -- Select a random table from Kavarna Rog
        SELECT id INTO user_id FROM AppUser ORDER BY RANDOM() LIMIT 1;
        -- Select a random user for the order
        SELECT NOW() - INTERVAL '5 months' * RANDOM() INTO order_date;
        -- Select a fixed order time for testing (adjust as needed)
        
        -- Determine the order status based on the order date
        IF order_date >= NOW() - INTERVAL '10 hours' THEN
            order_status := 'IN PROGRESS';
            item_status := 'pending';
        ELSE
            order_status := 'FINISHED';
            item_status := 'prepared';
        END IF;

        -- Insert a new order with the determined status
        INSERT INTO CustomerOrder (status, date, table_id, user_id)
        VALUES (order_status, order_date, table_id, user_id)
        RETURNING id INTO order_id;

        -- Insert 1 to 5 items for each order from Kavarna Rog
        FOR j IN 1..(FLOOR(RANDOM() * 5 + 1))::INTEGER LOOP
            -- Select a random item from Kavarna Rog's menu
            SELECT rm.item_id INTO menu_item_id FROM RestaurantMenu rm
            WHERE rm.restaurant_id = (SELECT id FROM Restaurant WHERE name = 'Kavarna Rog')
            ORDER BY RANDOM() LIMIT 1;
            
            -- Check if the item already exists in the order
            SELECT EXISTS (
                SELECT 1 FROM OrderItem oi WHERE oi.customer_order_id = order_id AND oi.item_id = menu_item_id
            ) INTO item_exists;

            -- If the item does not exist, insert it
            IF NOT item_exists THEN
                -- Generate a random quantity between 1 and 4
                SELECT FLOOR(RANDOM() * 4 + 1)::INTEGER INTO item_quantity;

                -- Insert the item with the determined status
                INSERT INTO OrderItem (customer_order_id, item_id, quantity, status)
                VALUES (order_id, menu_item_id, item_quantity, item_status);
            END IF;
        END LOOP;
    END LOOP;
END $$;


