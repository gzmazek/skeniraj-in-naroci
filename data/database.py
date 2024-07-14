import psycopg2
import psycopg2.extras
from typing import List

from .model import User, Restaurant, Item, Order, OrderItem

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