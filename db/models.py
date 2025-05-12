from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    # Отношения
    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", uselist=False, back_populates="user")


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    # Отношения
    product_categories = relationship("ProductCategory", back_populates="category")
    products = relationship("Product", secondary="product_categories", viewonly=True)


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(50), nullable=False, unique=True)

    # Отношения
    product_categories = relationship("ProductCategory", back_populates="product")
    categories = relationship("Category", secondary="product_categories", viewonly=True)
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")


class ProductCategory(Base):
    __tablename__ = 'product_categories'

    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)

    # Отношения
    product = relationship("Product", back_populates="product_categories")
    category = relationship("Category", back_populates="product_categories")


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(String, primary_key=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    order_status = Column(String(20), nullable=False)  # "В процессе", "Готов", "Отказ"
    is_special_order = Column(Boolean, nullable=True, default=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    completion_date = Column(DateTime, nullable=True)

    # Отношения
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    # Отношения
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


class Cart(Base):
    __tablename__ = 'carts'

    cart_id = Column(String, primary_key=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    user = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'

    cart_item_id = Column(String, primary_key=True)
    cart_id = Column(String, ForeignKey('carts.cart_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Отношения
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")