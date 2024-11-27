from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from database import engine, SesionLocal
from models import Product
from fastapi_jwt_auth import AuthJWT
from schemas import ProductSchema

session = SesionLocal(bind=engine)

product_router = APIRouter(
    prefix='/products'
)


@product_router.get('/')
def get_products():
    return {"message": "Hello Product page"}


@product_router.post('/create', response_model=ProductSchema)
async def create_product(product: ProductSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    new_product = Product(
        name=product.name,
        price=product.price
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    session.close()  # Ensure session is closed

    return new_product
