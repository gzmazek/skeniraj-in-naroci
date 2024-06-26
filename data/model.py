from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from dataclasses_json import dataclass_json

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
    allergen: Optional[str] = field(default=None)

@dataclass_json
@dataclass
class MenuItem:
    table_id: int = field(default=None)
    item_id: int = field(default=None)

@dataclass_json
@dataclass
class Order:
    id: int = field(default=None)
    status: str = field(default=None)
    date: datetime = field(default_factory=datetime.now)
    table_id: int = field(default=None)
    user_id: Optional[int] = field(default=None)

@dataclass_json
@dataclass
class OrderItem:
    order_id: int = field(default=None)
    item_id: int = field(default=None)
    quantity: int = field(default=None)
