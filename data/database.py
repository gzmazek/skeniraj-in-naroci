"""
DATABASE.PY - TABLE OF CONTENTS
================================

1. IMPORTS
--------------------------------
- psycopg2
- typing.List
- django.db.connection
- Other necessary imports...

2. UTILITIES
--------------------------------
- convert_decimal_to_float(value)

3. USER FUNCTIONS
--------------------------------
- addAppuser(user: User)
- getUserByEmail(email: str)
- getUserByID(user_id: int)
- changeUserPassword(user_id: int, new_pass: str)
- getUserOrders(user_id: int)
- getUserPopularRestaurants(user_id: int)

4. RESTAURANT FUNCTIONS
--------------------------------
- addRestaurant(restaurant: Restaurant)
- getRestaurantByID(restaurant_id: int)
- getRestaurantFromTableID(table_id: int)
- getRestaurantsOfOwner(user_id: int)
- getRestaurantMenu(restaurant_id: int)
- addItemToRestaurantMenu(restaurant_id: int, item: Item)
- removeItemFromRestaurantMenu(item_id: int, restaurant_id: int)

5. ORDER FUNCTIONS
--------------------------------
- addCustomerOrder(order: CustomerOrder)
- getOrdersByTableID(table_id: int)
- getItemsByOrderID(order_id: int)
- markOrderAsDelivered(order_id: int)
- update_order_status(order_id: int, status: str)
- update_order_items_status(order_id: int, status: str)
- addItemToOrder(orderItem: OrderItem)
- get_last_finished_order_by_table_id(table_id)

6. ITEM FUNCTIONS
--------------------------------
- addNewItem(item: Item)
- getItemNameByID(item_id: int)
- markItemAsPrepared(item_id, order_id)

7. TABLE FUNCTIONS
--------------------------------
- addTable(table: Table)
- getTablesByRestaurant(restaurant_id: int)
- getTableByID(table_id: int)
- deleteTable(table_id: int)
- updateTablePosition(table_id: int, position_x: int, position_y: int)

8. KITCHEN FUNCTIONS
--------------------------------
- get_kitchens_by_restaurant_id(restaurant_id: int)
- add_kitchen(restaurant_id: int, name: str)
- get_items_not_in_kitchen(restaurant_id: int, kitchen_id: int)
- add_item_to_kitchen(kitchen_id: int, item_id: int)
- remove_item_from_kitchen(kitchen_id: int, item_id: int)
- get_items_by_kitchen_id(kitchen_id: int)
- delete_kitchen_by_id(kitchen_id: int)
- get_kitchen_by_id(kitchen_id: int)
- get_ordered_items_by_kitchen_id(kitchen_id: int)

9. DATA ANALYTICS FUNCTIONS
--------------------------------
- get_item_revenue_by_restaurant(restaurant_id: int)
- get_avg_order_value_by_restaurant(restaurant_id: int)
- get_revenue_by_customer_type(restaurant_id: int)
- get_orders_per_hour(restaurant_id: int)
- get_revenue_per_hour(restaurant_id: int)
- get_common_item_pairs(restaurant_id: int)

"""
import psycopg2
import psycopg2.extras
from typing import List
from decimal import Decimal

from .model import User, Restaurant, CustomerOrder, OrderItem, Order, MenuItem, Table, Item, Kitchen

from django.db import connection

#########################################################
#                     UTILITIES                         #
#########################################################

def convert_decimal_to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

#########################################################
#                     USER FUNCTIONS                    #
#########################################################

## TODO: add exception catching, so that it returns some error if something goes wrong
def addAppuser(user: User):
    """
    Adds a user to the database.
    """
    with connection.cursor() as cursor:
        cmd = "INSERT INTO AppUser (email, name, surname, password) VALUES (%s, %s, %s, %s) RETURNING id"
        data = (user.email, user.name, user.surname, user.password)
        cursor.execute(cmd, data)
        user.id = cursor.fetchone()[0]
    return user

def getUserByEmail(email: str):
    """
    Returns user with given email if it exists
    """
    user = None
    with connection.cursor() as cursor:
        cmd = "SELECT * FROM AppUser WHERE email = %s"
        data = (email,)
        cursor.execute(cmd, data)
        user = cursor.fetchone()

    if user is None:
        return None
    else:
        user = User(user[0],user[1],user[2],user[3],user[4])
        return user
    
def getUserByID(user_id: int):
    """
    Returns user with given ID if it exists
    """
    user = None
    with connection.cursor() as cursor:
        cmd = "SELECT * FROM AppUser WHERE id = %s"
        data = (user_id,)
        cursor.execute(cmd, data)
        user = cursor.fetchone()

    if user is None:
        return None
    else:
        user = User(user[0],user[1],user[2],user[3],user[4])
        return user
    
def changeUserPassword(user_id: int, new_pass: str):
    """
    Changes the password of given user and returns it.
    """
    user = None
    with connection.cursor() as cursor:
        cmd = """
        UPDATE AppUser
        SET password = %s
        WHERE id = %s
        RETURNING *;
        """
        data = (new_pass, user_id)
        cursor.execute(cmd, data)
        user = cursor.fetchone()

    if user is None:
        return None
    else:
        user = User(user[0],user[1],user[2],user[3],user[4])
        return user
    
def getUserOrders(user_id: int):
    """
    Returns the list of all orders of user
    """
    orders = []
    with connection.cursor() as cursor:
        cmd = """
        SELECT
            co.id AS order_id,
            r.name AS restaurant_name,
            array_agg(i.name) AS item_names,
            array_agg(oi.quantity) AS item_quantities,
            array_agg(i.value * oi.quantity) AS item_total_prices,
            SUM(i.value * oi.quantity) AS total_price,
            co.date AS order_date
        FROM
            CustomerOrder co
        JOIN
            OrderItem oi ON co.id = oi.customer_order_id
        JOIN
            Item i ON oi.item_id = i.id
        JOIN
            DiningTable dt ON co.table_id = dt.id
        JOIN
            Restaurant r ON dt.restaurant_id = r.id
        WHERE
            co.user_id = %s
        GROUP BY
            co.id, r.name, co.date
        ORDER BY
            co.date DESC;
        """
        data = (user_id,)
        cursor.execute(cmd, data)
        ord = cursor.fetchall()

        for o in ord:
            order = Order(restaurant=o[1], date=o[6], total_value=o[5], items=o[2], item_quantities=o[3], item_values=o[4])
            orders.append(order)
    
    return orders

def getUserPopularRestaurants(user_id: int):
    """
    Gets restaurants in descending order based on how many times user has ordered from it.
    """
    restaurants = []
    with connection.cursor() as cursor:
        cmd = """ 
        SELECT
            r.id,
            r.name,
            r.location,
            r.owner_id,
            COUNT(co.id) AS order_count
        FROM
            CustomerOrder co
            JOIN DiningTable dt ON co.table_id = dt.id
            JOIN Restaurant r ON dt.restaurant_id = r.id
        WHERE
            co.user_id = %s
        GROUP BY
            r.id, r.name, r.location, r.owner_id
        ORDER BY
            order_count DESC;"""
        data = (user_id,)
        cursor.execute(cmd, data)
        data = cursor.fetchall()
        for d in data:
            restaurants.append(Restaurant(id=d[0], name=d[1], location=d[2], owner_id=d[3]))

    return restaurants

#########################################################
#                   RESTAURANT FUNCTIONS                #
#########################################################

def addRestaurant(restaurant: Restaurant):
    """
    Adds a new restaurant to the database
    """
    with connection.cursor() as cursor:
        cmd = "INSERT INTO Restaurant (name, location, owner_id) VALUES (%s, %s, %s) RETURNING id"
        data = (restaurant.name, restaurant.location, restaurant.owner_id)
        cursor.execute(cmd, data)
        restaurant.id = cursor.fetchone()[0]
    return restaurant

def getRestaurantByID(restaurant_id: int):
    """
    Returns restaurant with given ID
    """
    rest = None
    with connection.cursor() as cursor:
        cmd = "SELECT * FROM Restaurant WHERE id = %s"
        data = (restaurant_id,)
        cursor.execute(cmd, data)
        rest = cursor.fetchone()

    if rest is None:
        return None
    else:
        return Restaurant(rest[0],rest[1],rest[2],rest[3])

def getRestaurantFromTableID(table_id: int):
    """
    Gets the restaurant that given table belongs to if such a table actually exists
    """
    with connection.cursor() as cursor:
        cmd = """
        SELECT
            dt.id AS table_id,
            r.id AS restaurant_id,
            r.name AS name,
            r.location AS location,
            r.owner_id AS owner_id
        FROM DiningTable dt
        JOIN Restaurant r ON dt.restaurant_id = r.id
        WHERE dt.id = %s
        """
        data = (table_id,)
        cursor.execute(cmd, data)
        restaurant = cursor.fetchone()
        if restaurant == None:
            return None
        return Restaurant(id=restaurant[1], name=restaurant[2], location=restaurant[3], owner_id=restaurant[4])


def getRestaurantsOfOwner(user_id: int):
    """
    Returns the list of all restaurants owned by some user with user_id
    """
    restaurants = []
    with connection.cursor() as cursor:
        cmd = "SELECT * FROM Restaurant WHERE owner_id = %s"
        data = (user_id,)
        cursor.execute(cmd, data)
        list = cursor.fetchall()

        for el in list:
            restaurants.append(Restaurant(el[0], el[1], el[2], el[3]))

    return restaurants

def getRestaurantMenu(restaurant_id: int):
    """
    Returns the entire restaurant menu (list of menu items)
    """
    menu = []  
    with connection.cursor() as cursor:
        cmd = """
        SELECT
            i.id,
            i.name,
            i.value
        FROM Item i
        JOIN RestaurantMenu m ON i.id = m.item_id
        WHERE m.restaurant_id = %s
        """
        data = (restaurant_id,)
        cursor.execute(cmd, data)
        items = cursor.fetchall()
        for item in items:
            menu.append(MenuItem(id=item[0], name=item[1], value=convert_decimal_to_float(item[2])))

    return menu

def addItemToRestaurantMenu(restaurant_id: int, item: Item):
    """
    Adds an item to the restaurant menu
    """
    try:
        with connection.cursor() as cursor:
            cmd = "INSERT INTO RestaurantMenu (restaurant_id, item_id) VALUES (%s, %s)"
            data = (restaurant_id, item.id)
            cursor.execute(cmd, data)
            return True
    except Exception as e:
        print(f"Error adding item to restaurant menu: {e}")
        return False
    
def removeItemFromRestaurantMenu(item_id:int, restaurant_id:int):
    """
    Removes the item from menu of given restaurant
    """
    try:
        with connection.cursor() as cursor:
            # Update the order status to finished for given order
            cmd = "DELETE FROM RestaurantMenu WHERE restaurant_id = %s AND item_id = %s"
            cursor.execute(cmd, [restaurant_id, item_id])
        return True
    except Exception as e:
        print(f"Error deleting item from restaurant menu: {e}")
        return False

#########################################################
#                     ORDER FUNCTIONS                   #
#########################################################

def addCustomerOrder(order: CustomerOrder):
    """
    Adds a new customer order to the database
    """
    with connection.cursor() as cursor:
        cmd = "INSERT INTO CustomerOrder (table_id, user_id, status) VALUES (%s, %s, %s) RETURNING id"
        data = (order.table_id, order.user_id, order.status)
        cursor.execute(cmd, data)
        order.id = cursor.fetchone()[0]
    return order

def getOrdersByTableID(table_id: int) -> List[CustomerOrder]:
    """
    Returns the current orders for a given table, including associated items.
    """
    with connection.cursor() as cursor:
        # Fetch orders for the table
        cmd = """
        SELECT 
            co.id, co.status, co.date, co.table_id, co.user_id
        FROM 
            CustomerOrder co
        WHERE 
            co.table_id = %s AND co.status != 'FINISHED'
        ORDER BY 
            co.date ASC
        """
        cursor.execute(cmd, (table_id,))
        orders = cursor.fetchall()
    
    arr = []
    for order in orders:
        # Create the CustomerOrder object with its items
        arr.append(CustomerOrder(
            id=order[0],
            status=order[1],
            date=order[2],
            table_id=order[3],
            user_id=order[4],
        ))
    return arr

def getItemsByOrderID(order_id: int) -> List[OrderItem]:
    """
    Returns the items associated with a given order, including the item name.
    """
    with connection.cursor() as cursor:
        item_cmd = """
        SELECT 
            oi.item_id, oi.quantity, oi.status
        FROM 
            OrderItem oi
        WHERE 
            oi.customer_order_id = %s
        """
        cursor.execute(item_cmd, (order_id,))
        items = cursor.fetchall()

        # Convert the items into a list of OrderItem objects with item names
        order_items = []
        for item in items:
            order_items.append(OrderItem(
                item_id=item[0],
                quantity=item[1],
                status=item[2]
            ))
    
    return order_items

def markOrderAsDelivered(order_id):
    """
    Marks the order as delivered by updating the order status.
    """
    try:
        with connection.cursor() as cursor:
            # Update the order status to finished for given order
            cmd = "UPDATE CustomerOrder SET status = 'FINISHED' WHERE id = %s"
            cursor.execute(cmd, [order_id])
        return True
    except Exception as e:
        print(f"Error marking order as delivered: {e}")
        return False
    
def update_order_status(order_id, status):
    """
    Updates the status of a specific order in the database.
    """
    try:
        with connection.cursor() as cursor:
            cmd = """
            UPDATE CustomerOrder 
            SET status = %s 
            WHERE id = %s
            """
            cursor.execute(cmd, [status, order_id])
        return True
    except Exception as e:
        print(f"Error updating order status: {e}")
        return False

def update_order_items_status(order_id, status):
    """
    Updates the status of all items in a specific order in the database.
    """
    try:
        with connection.cursor() as cursor:
            cmd = """
            UPDATE OrderItem 
            SET status = %s 
            WHERE customer_order_id = %s
            """
            cursor.execute(cmd, [status, order_id])
        return True
    except Exception as e:
        print(f"Error updating order items status: {e}")
        return False

def addItemToOrder(orderItem: OrderItem):
    """
    Adds new order item to database. 
    Explanation: Every customer order has multiple order items, hence this items must be mapped together 
    """
    with connection.cursor() as cursor:
        cmd = "INSERT INTO OrderItem (customer_order_id, item_id, quantity) VALUES (%s, %s, %s)"
        data = (orderItem.order_id, orderItem.item_id, orderItem.quantity)
        cursor.execute(cmd, data)

def get_last_finished_order_by_table_id(table_id):
    """
    Finds the last finished order associated with a given table.
    """
    try:
        with connection.cursor() as cursor:
            cmd = """
            SELECT id, status, date
            FROM CustomerOrder
            WHERE table_id = %s AND status = 'FINISHED'
            ORDER BY date DESC
            LIMIT 1
            """
            cursor.execute(cmd, [table_id])
            order = cursor.fetchone()
            
            if order is not None:
                return {
                    'id': order[0],
                    'status': order[1],
                    'date': order[2]
                }
            else:
                return None
    except Exception as e:
        print(f"Error fetching last finished order: {e}")
        return None

#########################################################
#                    ITEM FUNCTIONS                     #
#########################################################

def addNewItem(item: Item):
    """
    Adds a new item to the database. Returns the item added.
    """
    with connection.cursor() as cursor:
        cmd = "INSERT INTO Item (name, value) VALUES (%s, %s) RETURNING id"
        data = (item.name, item.value)
        cursor.execute(cmd, data)
        item.id = cursor.fetchone()[0]
    return item

def getItemNameByID(item_id: int) -> str:
    """
    Returns the name of the item given its ID.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Item WHERE id = %s", (item_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

def markItemAsPrepared(item_id, order_id):
    """
    Marks a specific order item as prepared in the database.
    If all items in the order are prepared, marks the entire order as prepared.
    """
    try:
        with connection.cursor() as cursor:
            # Mark the specific item as prepared
            cmd = "UPDATE OrderItem SET status = 'prepared' WHERE item_id = %s AND customer_order_id = %s"
            cursor.execute(cmd, [item_id, order_id])

            # Check if all items in this order are now prepared
            check_cmd = """
            SELECT COUNT(*) 
            FROM OrderItem 
            WHERE customer_order_id = %s AND status != 'prepared'
            """
            cursor.execute(check_cmd, [order_id])
            not_prepared_count = cursor.fetchone()[0]

            if not_prepared_count == 0:
                # If all items are prepared, update the order status to 'PREPARED'
                update_order_cmd = "UPDATE CustomerOrder SET status = 'PREPARED' WHERE id = %s"
                cursor.execute(update_order_cmd, [order_id])

            connection.commit()
        return True
    except Exception as e:
        print(f"Error marking item as prepared: {e}")
        return False

#########################################################
#                     TABLE FUNCTIONS                   #
#########################################################

def addTable(table: Table):
    """
    Adds a new dining table to the restaurant.
    """
    with connection.cursor() as cursor:
        if table.position_x is None or table.position_y is None:
            table.position_x = 1  
            table.position_y = 1  
        cmd = "INSERT INTO DiningTable (restaurant_id, position_x, position_y) VALUES (%s, %s, %s) RETURNING id"
        data = (table.restaurant_id, table.position_x, table.position_y)
        cursor.execute(cmd, data)
        table.id = cursor.fetchone()[0]
    return table

def getTablesByRestaurant(restaurant_id: int):
    """
    Returns the list of tables that belong to given restaurant
    """
    tables = []
    with connection.cursor() as cursor:
        cmd = "SELECT id, restaurant_id, position_x, position_y FROM DiningTable WHERE restaurant_id = %s"
        data = (restaurant_id,)
        cursor.execute(cmd, data)
        rows = cursor.fetchall()
        for row in rows:
            tables.append(Table(id=row[0], restaurant_id=row[1], position_x=row[2], position_y=row[3]))
    return tables

def getTableByID(table_id: int):
    """
    Returns the table with given id if it exists.
    """
    with connection.cursor() as cursor:
        cmd = "SELECT id, restaurant_id, position_x, position_y FROM DiningTable WHERE id = %s"
        data = (table_id,)
        cursor.execute(cmd, data)
        row = cursor.fetchone()
    if row:
        return Table(id=row[0], restaurant_id=row[1], position_x=row[2], position_y=row[3])
    return None

def deleteTable(table_id: int):
    """
    Deletes the table from the database.
    """
    with connection.cursor() as cursor:
        cmd = "DELETE FROM DiningTable WHERE id = %s"
        data = (table_id,)
        cursor.execute(cmd, data)

def updateTablePosition(table_id: int, position_x: int, position_y: int):
    """
    Updates the position of a table in the database.
    """
    with connection.cursor() as cursor:
        cmd = "UPDATE DiningTable SET position_x = %s, position_y = %s WHERE id = %s"
        data = (position_x, position_y, table_id)
        cursor.execute(cmd, data)

#########################################################
#                     KITCHEN FUNCTIONS                 #
#########################################################

def get_kitchens_by_restaurant_id(restaurant_id):
    """
    Retrieves all kitchens associated with a restaurant.
    """
    with connection.cursor() as cursor:
        cmd = "SELECT id, restaurant_id, name FROM kitchen WHERE restaurant_id = %s"
        cursor.execute(cmd, [restaurant_id])
        kitchens = cursor.fetchall()
        return [Kitchen(id=k[0], restaurant_id=k[1], name=k[2]) for k in kitchens]

def add_kitchen(restaurant_id, name):
    """
    Adds a new kitchen to a restaurant.
    """
    try:
        with connection.cursor() as cursor:
            cmd = "INSERT INTO kitchen (restaurant_id, name) VALUES (%s, %s) RETURNING id"
            cursor.execute(cmd, [restaurant_id, name])
            kitchen_id = cursor.fetchone()[0]
            return kitchen_id
    except Exception as e:
        print(f"Error adding kitchen: {e}")
        return None

def get_items_not_in_kitchen(restaurant_id, kitchen_id):
    """
    Retrieves items that are in the restaurant's menu but not yet associated with the given kitchen.
    Returns a list of Item objects.
    """
    with connection.cursor() as cursor:
        cmd = """
        SELECT i.id, i.name
        FROM Item i
        JOIN RestaurantMenu rm ON i.id = rm.item_id
        WHERE rm.restaurant_id = %s
        AND i.id NOT IN (
            SELECT item_id FROM kitchenitem WHERE kitchen_id = %s
        )
        """
        cursor.execute(cmd, [restaurant_id, kitchen_id])
        items = cursor.fetchall()

        # Convert the result into a list of Item objects
        return [Item(id=item[0], name=item[1]) for item in items]

def add_item_to_kitchen(kitchen_id, item_id):
    """
    Adds an item to a kitchen.
    """
    try:
        with connection.cursor() as cursor:
            cmd = "INSERT INTO kitchenitem (kitchen_id, item_id) VALUES (%s, %s)"
            cursor.execute(cmd, [kitchen_id, item_id])
        return True
    except Exception as e:
        print(f"Error adding item to kitchen: {e}")
        return False
    
def remove_item_from_kitchen(kitchen_id, item_id):
    """
    Removes an item from a kitchen.
    """
    try:
        with connection.cursor() as cursor:
            cmd = "DELETE FROM kitchenitem WHERE kitchen_id = %s AND item_id = %s"
            cursor.execute(cmd, [kitchen_id, item_id])
        return True
    except Exception as e:
        print(f"Error removing item from kitchen: {e}")
        return False

def get_items_by_kitchen_id(kitchen_id):
    """
    Returns list of items for given kitchen.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT i.id, i.name
            FROM kitchenitem ki
            JOIN item i ON ki.item_id = i.id
            WHERE ki.kitchen_id = %s
        """, [kitchen_id])
        items = cursor.fetchall()
    return [Item(id=row[0], name=row[1]) for row in items]

def delete_kitchen_by_id(kitchen_id):
    """
    Deletes a kitchen and its associated items by kitchen ID.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM kitchenitem WHERE kitchen_id = %s", [kitchen_id])
            cursor.execute("DELETE FROM kitchen WHERE id = %s", [kitchen_id])
            connection.commit() 
            return True
        except Exception as e:
            print(f"Error deleting kitchen: {e}")
            connection.rollback() 
            # .rollback, da ne samo dela  deleta, recimo da ne samo itemov, kitchena pa potem ne bi moglo
            return False

def get_kitchen_by_id(kitchen_id: int) -> Kitchen:
    """
    Retrieves a specific kitchen by its ID.

    Args:
        kitchen_id (int): The ID of the kitchen to retrieve.

    Returns:
        Kitchen: The Kitchen object if found, otherwise None.
    """
    with connection.cursor() as cursor:
        cmd = "SELECT id, restaurant_id, name FROM kitchen WHERE id = %s"
        cursor.execute(cmd, [kitchen_id])
        kitchen = cursor.fetchone()
        
        if kitchen:
            return Kitchen(id=kitchen[0], restaurant_id=kitchen[1], name=kitchen[2])
        else:
            return None

# KITCHEN VIEW, ta funkcija je za vsa naročila v enem kitchenu
def get_ordered_items_by_kitchen_id(kitchen_id):
    """
    Retrieves ordered items associated with a given kitchen, excluding delivered items.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT i.id, i.name, oi.customer_order_id, oi.quantity, oi.status
            FROM kitchenitem ki
            JOIN item i ON ki.item_id = i.id
            JOIN orderitem oi ON i.id = oi.item_id
            JOIN customerorder co ON oi.customer_order_id = co.id
            WHERE ki.kitchen_id = %s AND co.status != 'FINISHED'
        """, [kitchen_id])
        items = cursor.fetchall()

    # Return a list of dictionaries with the relevant data
    return [
        {
            'id': row[0],
            'item_name': row[1],
            'order_id': row[2],
            'quantity': row[3],
            'status': row[4],
        }
        for row in items
    ]

#########################################################
#                 DATA ANALYTICS FUNCTIONS              #
#########################################################

def get_item_revenue_by_restaurant(restaurant_id):
    """
    Retrieves the total revenue generated by each item in a given restaurant.
    """
    with connection.cursor() as cursor:
        query = """
            SELECT 
                r.name AS restaurant_name,
                i.name AS item_name,
                SUM(oi.quantity * i.value) AS total_revenue
            FROM 
                OrderItem oi
            JOIN 
                Item i ON oi.item_id = i.id
            JOIN 
                CustomerOrder co ON oi.customer_order_id = co.id
            JOIN 
                DiningTable dt ON co.table_id = dt.id
            JOIN 
                Restaurant r ON dt.restaurant_id = r.id
            WHERE 
                r.id = %s
            GROUP BY 
                r.name, i.name
            ORDER BY 
                total_revenue DESC;
        """
        cursor.execute(query, [restaurant_id])
        result = cursor.fetchall()

    print(result)
    return result

def get_avg_order_value_by_restaurant(restaurant_id):
    """
    Retrieves the average order value for a given restaurant.
    """
    with connection.cursor() as cursor:
        query = """
            SELECT 
                r.name AS restaurant_name,
                AVG(oi.quantity * i.value) AS avg_order_value
            FROM 
                OrderItem oi
            JOIN 
                Item i ON oi.item_id = i.id
            JOIN 
                CustomerOrder co ON oi.customer_order_id = co.id
            JOIN 
                DiningTable dt ON co.table_id = dt.id
            JOIN 
                Restaurant r ON dt.restaurant_id = r.id
            WHERE 
                r.id = %s
            GROUP BY 
                r.name
            ORDER BY 
                avg_order_value DESC;
        """
        cursor.execute(query, [restaurant_id])
        result = cursor.fetchall()
    return result

def get_revenue_by_customer_type(restaurant_id):
    """
    Retrieves total revenue categorized by new and returning customers for a given restaurant.
    """
    with connection.cursor() as cursor:
        query = """
            WITH first_order AS (
                SELECT 
                    user_id, 
                    MIN(date) AS first_order_date
                FROM 
                    CustomerOrder
                GROUP BY 
                    user_id
            )
            SELECT 
                CASE 
                    WHEN co.date = fo.first_order_date THEN 'New Customer'
                    ELSE 'Returning Customer'
                END AS customer_type,
                SUM(oi.quantity * i.value) AS total_revenue
            FROM 
                CustomerOrder co
            JOIN 
                OrderItem oi ON co.id = oi.customer_order_id
            JOIN 
                Item i ON oi.item_id = i.id
            JOIN 
                DiningTable dt ON co.table_id = dt.id
            JOIN 
                first_order fo ON co.user_id = fo.user_id
            WHERE 
                dt.restaurant_id = %s
            GROUP BY 
                customer_type
            ORDER BY 
                total_revenue DESC;
        """
        cursor.execute(query, [restaurant_id])
        result = cursor.fetchall()
    return result

def get_orders_per_hour(restaurant_id):
    query = """
    SELECT 
        EXTRACT(HOUR FROM co.date) AS order_hour,
        COUNT(co.id) AS order_count
    FROM 
        CustomerOrder co
    JOIN 
        DiningTable dt ON co.table_id = dt.id
    WHERE 
        dt.restaurant_id = %s
    GROUP BY 
        order_hour
    ORDER BY 
        order_hour;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (restaurant_id,))
        return cursor.fetchall()

def get_revenue_per_hour(restaurant_id):
    query = """
    SELECT 
        EXTRACT(HOUR FROM co.date) AS order_hour,
        SUM(oi.quantity * i.value) AS total_revenue
    FROM 
        CustomerOrder co
    JOIN 
        OrderItem oi ON co.id = oi.customer_order_id
    JOIN 
        Item i ON oi.item_id = i.id
    JOIN 
        DiningTable dt ON co.table_id = dt.id
    WHERE 
        dt.restaurant_id = %s
    GROUP BY 
        order_hour
    ORDER BY 
        order_hour;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (restaurant_id,))
        return cursor.fetchall()
    
def get_common_item_pairs(restaurant_id):
    """
    Fetches the most common pairs of items ordered together for a specific restaurant.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH item_pairs AS (
                SELECT 
                    oi1.item_id AS item_1,
                    oi2.item_id AS item_2,
                    COUNT(*) AS pair_count
                FROM 
                    OrderItem oi1
                JOIN 
                    OrderItem oi2 ON oi1.customer_order_id = oi2.customer_order_id AND oi1.item_id < oi2.item_id
                JOIN 
                    CustomerOrder co ON oi1.customer_order_id = co.id
                JOIN 
                    DiningTable dt ON co.table_id = dt.id
                WHERE 
                    dt.restaurant_id = %s
                GROUP BY 
                    oi1.item_id, oi2.item_id
            )
            SELECT 
                i1.name AS item_1_name,
                i2.name AS item_2_name,
                pair_count
            FROM 
                item_pairs
            JOIN 
                Item i1 ON item_pairs.item_1 = i1.id
            JOIN 
                Item i2 ON item_pairs.item_2 = i2.id
            ORDER BY 
                pair_count DESC
            LIMIT 10;
        """, [restaurant_id])
        return cursor.fetchall()

#########################################################