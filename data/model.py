from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from dataclasses_json import dataclass_json
from typing import List

# dataclass representations of all tables in database

@dataclass_json
@dataclass
class User:
    id: int = field(default=None)
    email: str = field(default=None)
    name: str = field(default=None)
    surname: str = field(default=None)
    password: str = field(default=None)

@dataclass_json
@dataclass
class Restaurant:
    id: int = field(default=None)
    name: str = field(default=None)
    location: str = field(default=None)
    owner_id: Optional[int] = field(default=None)

@dataclass_json
@dataclass
class Table:
    id: int = field(default=None)
    restaurant_id: int = field(default=None)

@dataclass_json
@dataclass
class Item:
    id: int = field(default=None)
    name: str = field(default=None)
    value: float = field(default=None)
    tags: str = field(default=b'\x00\x00\x00\x00')

@dataclass_json
@dataclass
class RestaurantItem:
    restaurant_id: int = field(default=None)
    item_id: int = field(default=None)

@dataclass_json
@dataclass
class CustomerOrder:
    id: int = field(default=None)
    status: str = field(default=None)
    date: datetime = field(default_factory=datetime.now)
    table_id: Optional[int] = field(default=None)
    user_id: Optional[int] = field(default=None)

@dataclass_json
@dataclass
class OrderItem:
    order_id: int = field(default=None)
    item_id: int = field(default=None)
    quantity: int = field(default=None)

# dataclass representation of other classes used in this project

@dataclass_json
@dataclass
class Order:
    restaurant: str = field(default=None)
    date: datetime = field(default=None)
    total_value: float = field(default=None)
    items: List[str] = field(default_factory=list)
    item_quantities: List[int] = field(default_factory=list) 
    item_values: List[float] = field(default_factory=list)

