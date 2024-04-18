import django.utils.timezone
import json
from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from slugify import slugify
from django.utils.timezone import now

class Blog(BaseModel):
    class Config:
        orm_mode = True
    name: str
    slug: str
    status: str='draft'
    ordering: int = 0
    special: bool
    publish_date: datetime
    content: str
    image: Optional[str]

    def __init__(self, **data):
        if data["slug"] is None:
            data["slug"] = slugify(data["name"])
        super().__init__(**data)

class Category(BaseModel):
    class Config:
        orm_mode = True
    name: str
    slug: str
    is_homepage: bool
    status: str='draft'
    ordering: int = 0

    def __init__(self, **data):
        if data["slug"] is None:
            data["slug"] = slugify(data["name"])
        super().__init__(**data)

    def generate_slug(self):
        self.slug = slugify(self.name)

class Contact(BaseModel):
    class Config:
        orm_mode = True
    name: str
    email: str
    phone: str
    message: str
    contacted: bool
    message_admin: str = ""
    created: datetime = now

class OrderItem(BaseModel):
    class Config:
        orm_mode = True
    order_id: int
    product_id: int
    quantity: int
    price: int
    total: int

class Order(BaseModel):
    class Config:
        orm_mode = True
    name: str
    code: str
    email: str
    address: str
    phone: str
    quantity: int = 0
    total: int = 0
    status: str = 'order'
    created: datetime = now

class PlantingMethod(BaseModel):
    class Config:
        orm_mode = True
    name: str
    slug: str
    is_homepage: bool
    status: str = 'draft'
    ordering: int = 0

class Product(BaseModel):
    class Config:
        orm_mode = True    
    name: str
    slug: str
    status: str
    ordering: int = 0
    special: bool
    price: int
    price_sale: Optional[int] = None
    price_real: int
    total_sold: int = 0
    summary: str
    content: str
    image: Optional[str] = None
    category_id: int
    planting_methods: List[int] = []

    def __init__(self, **data):
        if "price_sale" in data and data["price_sale"] is not None:
            data["price_real"] = data["price_sale"]
        else:
            data["price_real"] = data["price"]
        super().__init__(**data)
