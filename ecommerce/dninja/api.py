from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Form, File
from ninja.files import UploadedFile
from .schema import CategorySchema, ProductSchema
from ecommerce.inventory.models import Category, Product, Media
from typing import List
from django.shortcuts import get_object_or_404

api = NinjaAPI()

@api.post("/inventory/category")
def post_category(request, data: CategorySchema):
    qs = Category.objects.create(**data.dict())
    return {"name":qs.name}

@api.post("/inventory/product")
def post_product(request, data: ProductSchema):
    qs = Product.objects.create(**data.dict())
    return {"name": qs.name}

@api.get("inventory/category/all/", response=List[CategorySchema])
def get_category_list(request):
    qs = Category.objects.all()
    return qs

@api.get("/inventory/products/category/{category_slug}", response=List[ProductSchema])
def get_product_by_category(request, category_slug: str):
    qs = Product.objects.filter(category__slug=category_slug)
    return qs

@api.put("/inventory/category/{category_id}")
def update_category(request, category_id: int, payload: CategorySchema):
    category = get_object_or_404(Category, id=category_id)
    for attr, value in payload.dict().items():
        if value:
            setattr(category, attr, value)
    category.save()
    return {"Success": True}

@api.delete("/category/{cat_id}")
def delete_cat(request, cat_id: int):
    category = get_object_or_404(Category, id=cat_id)
    category.delete()
    return {"Success": True}

@api.post("inventory/category/form/")
def post_category_form(request, form: CategorySchema = Form(...)):
    category = Category.objects.create(**form.dict())
    return {"name": category.name}

@api.post("inventory/category/form/params/")
def post_category_form_params(request, name: str = Form(...), slug: str = Form(...)):
    category = Category.objects.create(name=name, slug=slug)
    return {"name": category.name}

@api.post("/upload/media")
def upload_media(request, prod_id: int = Form(...), file: UploadedFile = File(...)):
    product = get_object_or_404(Product, id=prod_id)
    media = Media.objects.create(product_inventory=product, img_url=file)
    return {"id": media.id}

@api.post("/upload/media/multiple")
def upload_media_multiple(request, prod_id: int = Form(...), files: List[UploadedFile] = File(...)):
    product = get_object_or_404(Product, id=prod_id)

    for img in files:
        Media.objects.create(product_inventory=product, img_url=img)

    return {"success": True}