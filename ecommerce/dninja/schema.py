from ninja import Schema, ModelSchema

from ecommerce.inventory.models import Product

class CategorySchema(Schema):
    name: str
    slug: str

class ProductSchema(ModelSchema):
    class Config:
        model = Product
        model_fields = ["name", "web_id", "category"]
