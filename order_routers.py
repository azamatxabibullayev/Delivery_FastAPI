from fastapi import APIRouter

order_router = APIRouter(
    prefix='/orders'
)


@order_router.get('/')
async def get_orders():
    return {'message': 'Welcome to the orders endpoint!'}


@order_router.get('/c')
async def create_order():
    return {'message': 'Order created successfully!'}
