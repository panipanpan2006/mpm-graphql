from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
import dataclasses

app = FastAPI()

# ====== DATA DUMMY ======
categories = [
    {"id": 1, "name": "Elektronik"},
    {"id": 2, "name": "Aksesoris"},
]

products = [
    {"id": 1, "name": "Laptop", "price": 1200.0, "category_id": 1},
    {"id": 2, "name": "Mouse",  "price": 25.0,   "category_id": 2},
]

# ====== STRAWBERRY TYPES ======
@strawberry.type
class Category:
    id: int
    name: str

@strawberry.type
class Product:
    id: int
    name: str
    price: float
    category: Optional[Category]

# ====== HELPER FUNCTIONS ======
def find_category_by_id(cid: int) -> Optional[Category]:
    for c in categories:
        if c["id"] == cid:
            cat = Category.__new__(Category)
            object.__setattr__(cat, 'id', c["id"])
            object.__setattr__(cat, 'name', c["name"])
            return cat
    return None

def make_category(c: dict) -> Category:
    obj = Category.__new__(Category)
    object.__setattr__(obj, 'id', c["id"])
    object.__setattr__(obj, 'name', c["name"])
    return obj

def make_product(p: dict) -> Product:
    obj = Product.__new__(Product)
    object.__setattr__(obj, 'id', p["id"])
    object.__setattr__(obj, 'name', p["name"])
    object.__setattr__(obj, 'price', p["price"])
    object.__setattr__(obj, 'category', find_category_by_id(p["category_id"]))
    return obj

# ====== QUERY ======
@strawberry.type
class Query:
    @strawberry.field
    def get_products(self) -> List[Product]:
        return [make_product(p) for p in products]

    @strawberry.field
    def get_product(self, id: int) -> Optional[Product]:
        for p in products:
            if p["id"] == id:
                return make_product(p)
        return None

    @strawberry.field
    def get_categories(self) -> List[Category]:
        return [make_category(c) for c in categories]

# ====== MUTATION ======
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_product(self, name: str, price: float, category_id: int) -> Product:
        new_id = max([p["id"] for p in products], default=0) + 1
        new_p  = {"id": new_id, "name": name, "price": price, "category_id": category_id}
        products.append(new_p)
        return make_product(new_p)

    @strawberry.mutation
    def add_category(self, name: str) -> Category:
        new_id = max([c["id"] for c in categories], default=0) + 1
        new_c  = {"id": new_id, "name": name}
        categories.append(new_c)
        return make_category(new_c)

# ====== SCHEMA & ROUTER ======
schema      = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")