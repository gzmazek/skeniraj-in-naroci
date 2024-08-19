import psycopg2
import psycopg2.extras
from typing import List

from .model import User, Restaurant, CustomerOrder, OrderItem, Order, MenuItem, Table, Item

from .auth_public import db, host, user, password

from django.db import connection

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

from decimal import Decimal

def convert_decimal_to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

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

def addItemToOrder(orderItem: OrderItem):
    """
    Adds new order item to database. 
    Explanation: Every customer order has multiple order items, hence this items must be mapped together 
    """
    with connection.cursor() as cursor:
        cmd = "INSERT INTO OrderItem (customer_order_id, item_id, quantity) VALUES (%s, %s, %s)"
        data = (orderItem.order_id, orderItem.item_id, orderItem.quantity)
        cursor.execute(cmd, data)

def addTable(table: Table):
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
    with connection.cursor() as cursor:
        cmd = "SELECT id, restaurant_id, position_x, position_y FROM DiningTable WHERE id = %s"
        data = (table_id,)
        cursor.execute(cmd, data)
        row = cursor.fetchone()
    if row:
        return Table(id=row[0], restaurant_id=row[1], position_x=row[2], position_y=row[3])
    return None

def deleteTable(table_id: int):
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

def getOrderByTableID_ex(table_id: int):
    """
    Returns the current order for a given table if it exists, including items.
    """
    with connection.cursor() as cursor:
        cmd = """
        SELECT 
            co.id, co.status, co.date, co.table_id, co.user_id
        FROM 
            CustomerOrder co
        WHERE 
            co.table_id = %s AND co.status != 'completed'
        ORDER BY 
            co.date DESC
        LIMIT 1
        """
        data = (table_id,)
        cursor.execute(cmd, data)
        order = cursor.fetchone()
    
    if order:
        order_id = order[0]
        items = []
        with connection.cursor() as cursor:
            cmd = """
            SELECT 
                oi.id, oi.name, oi.is_prepared
            FROM 
                OrderItem oi
            WHERE 
                oi.order_id = %s
            """
            cursor.execute(cmd, (order_id,))
            items = cursor.fetchall()
        
        return {
            'id': order[0],
            'status': order[1],
            'date': order[2],
            'table_id': order[3],
            'user_id': order[4],
            'items': [{'id': item[0], 'name': item[1], 'is_prepared': item[2]} for item in items]
        }
    return None

def getOrdersByTableID_v0(table_id: int):
    """
    Returns the current orders for a given table if it exists
    """
    with connection.cursor() as cursor:
        cmd = """
        SELECT 
            co.id, co.status, co.date, co.table_id, co.user_id
        FROM 
            CustomerOrder co
        WHERE 
            co.table_id = %s AND co.status != 'FINISHED'
        ORDER BY 
            co.date DESC
        """
        data = (table_id,)
        cursor.execute(cmd, data)
        orders = cursor.fetchall()
    
    arr = []
    for order in orders:
        arr.append(CustomerOrder(
            id=order[0],
            status=order[1],
            date=order[2],
            table_id=order[3],
            user_id=order[4]
        ))
    return arr

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
        order_id = order[0]

        # Use the new function to fetch the items for this order
        # order_items = getItemsByOrderID(order_id)

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

def getItemNameByID(item_id: int) -> str:
    """
    Returns the name of the item given its ID.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Item WHERE id = %s", (item_id,))
        result = cursor.fetchone()
        if result:
            return result[0]  # The name of the item
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

            connection.commit()  # Commit all changes to the database
        return True
    except Exception as e:
        print(f"Error marking item as prepared: {e}")
        return False

# Never used and incorrectly implemented
def markOrderAsPrepared(table_id):
    """
    Marks all items in an order for a given table as prepared and updates the order status.
    """
    try:
        with connection.cursor() as cursor:
            # Update the order status to 'prepared' for orders at the table that are not yet completed
            cmd = "UPDATE CustomerOrder SET status = 'PREPARED' WHERE table_id = %s AND status != 'FINISHED'"
            cursor.execute(cmd, [table_id])

            # Update all associated items to 'prepared'
            cmd = """
            UPDATE OrderItem
            SET status = 'prepared'
            WHERE order_id IN (
                SELECT id FROM CustomerOrder WHERE table_id = %s AND status = 'PREPARED'
            )
            """
            cursor.execute(cmd, [table_id])

        return True
    except Exception as e:
        print(f"Error marking order as prepared: {e}")
        return False

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
