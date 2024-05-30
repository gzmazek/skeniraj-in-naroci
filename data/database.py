import psycopg2
import psycopg2.extras
from typing import List

from model import User, Restaurant, Table, Item, MenuItem, Order, OrderItem

from .auth_public import db, host, user, password


class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(database=db, host=host, user=user, password=password)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def add_appuser(self, user: User):
        """
        Adds a user to the database.
        """
        cmd = "INSERT INTO AppUser (username, name, password, gender) VALUES (%s, %s, %s, %s) RETURNING id"
        data = (user.username, user.name, user.password, user.gender)
        self.cur.execute(cmd, data)
        user.id = self.cur.fetchone()[0]
        self.conn.commit()
        return user.id
    
#### Predelal sem samo tega prvega, pri drugih so še imena napačna, edina pravilna so v create_db.sql

    def add_item(self, item: Item):
        """
        Adds an item to the 'Item' table.
        """
        cmd = "INSERT INTO Item (name, value, allergen) VALUES (%s, %s, %s) RETURNING id"
        data = (item.name, item.value, item.allergen)
        self.cur.execute(cmd, data)
        item.id = self.cur.fetchone()[0]
        self.conn.commit()
        return item.id

    def place_order(self, order: Order, items: List[OrderItem]):
        """
        Places an order and records all associated items.
        """
        order_cmd = "INSERT INTO Order (status, date, table_id, user_id) VALUES (%s, %s, %s, %s) RETURNING id"
        order_data = (order.status, order.date, order.table_id, order.user_id)
        self.cur.execute(order_cmd, order_data)
        order.id = self.cur.fetchone()[0]

        for item in items:
            item_cmd = "INSERT INTO OrderItem (order_id, item_id, quantity) VALUES (%s, %s, %s)"
            item_data = (order.id, item.item_id, item.quantity)
            self.cur.execute(item_cmd, item_data)

        self.conn.commit()
        return order.id

    def get_users(self):
        """
        Retrieves all users from the 'User' table.
        """
        cmd = "SELECT * FROM User"
        self.cur.execute(cmd)
        users = [User.from_dict(row) for row in self.cur.fetchall()]
        return users

    def close(self):
        """
        Closes the database connection.
        """
        self.cur.close()
        self.conn.close()
