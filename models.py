from database import Base
from enum import Enum as PyEnum
from datetime import datetime,timezone
from sqlalchemy import Column, Integer, String, ForeignKey,Numeric,Boolean,Enum,DateTime,CheckConstraint
from sqlalchemy.orm import relationship


class UserRole(PyEnum):
    user = "user"
    admin = "admin"


class OrderStatus(PyEnum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String,nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    username = Column(String,nullable=False)
    email = Column(String, unique=True, nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    description = Column(String)
    price = Column(Numeric(10,2),nullable=False)
    stock = Column(Integer,nullable=False)
    image_url = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    __table_args__ = (CheckConstraint("stock >= 0", name="check_stock_nonnegative"),)


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True,nullable=False)
    user = relationship("User")
    items = relationship("CartItem", cascade="all, delete-orphan"   )


class CartItem(Base):
    __tablename__ = "cart_items"
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)
    product = relationship("Product")
    __table_args__ = (CheckConstraint("quantity > 0", name="check_quantity_positive"), )


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    total_price = Column(Numeric(10,2), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    items = relationship("OrderItem", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product")
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    __table_args__ = (CheckConstraint("quantity > 0", name="check_quantity_positive"), )