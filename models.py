from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(Text)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    orders = relationship("Order", back_populates='user')

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text)
    price = Column(Float)
    orders = relationship("Order", back_populates='product')

    def __repr__(self):
        return f"<Product(name='{self.name}', price='{self.price}')>"


class Order(Base):
    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered'),
        ('CANCELLED', 'cancelled')
    )
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    status = Column(ChoiceType(ORDER_STATUS), default='PENDING')
    user = relationship("User", back_populates='orders')
    product = relationship("Product", back_populates='orders')
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Order(user_id='{self.user_id}', product_id='{self.product_id}', status='{self.status}')>"
