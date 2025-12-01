from db import db
from decimal import Decimal
from datetime import datetime as dt


class Category(db.Model):
    __tablename__ = "categories"

    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(50), unique=True, nullable=False)

    products = db.relationship("Product", back_populates="category")


class Product(db.Model):
    __tablename__ = "products"

    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(100), nullable=False)
    price = db.mapped_column(db.DECIMAL(6, 2), nullable=False)
    inventory = db.mapped_column(db.Integer, nullable=False)

    category_id = db.mapped_column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="products")


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(100), nullable=False)
    phone = db.mapped_column(db.String, nullable=False)
    email = db.mapped_column(db.String(100), nullable=False)

    # REQUIRED for order relationship
    orders = db.relationship("Order", back_populates="customer")

    
    def pending_orders(self):
        return [o for o in self.orders if o.completed is None]

    def completed_orders(self):
        return [o for o in self.orders if o.completed is not None]



class Order(db.Model):
    __tablename__ = "orders"     # RECOMMENDED: use plural table name

    id = db.mapped_column(db.Integer, primary_key=True)

    # Corrected foreign key
    customer_id = db.mapped_column(
        db.ForeignKey("customers.id"),
        nullable=False
    )

    customer = db.relationship("Customer", back_populates="orders")

    created = db.mapped_column(db.DateTime, nullable=False, default=db.func.now())
    completed = db.mapped_column(db.DateTime, nullable=True, default=None)
    amount = db.mapped_column(db.DECIMAL(6, 2), nullable=True, default=None)

    items = db.relationship(
        "ProductOrder",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    def estimate(self):
        total = Decimal("0.00")
        for p in self.items:
            total += p.product.price * p.quantity
        return total

    def complete(self):
        if self.completed is not None:
            raise ValueError("Order is already completed.")

        # 1. Check inventory
        for p in self.items:
            if p.quantity > p.product.inventory:
                raise ValueError(
                    f"Not enough stock for '{p.product.name}'. "
                    f"Requested {p.quantity}, in stock {p.product.inventory}."
                )

        # 2. Subtract inventory
        for p in self.items:
            p.product.inventory -= p.quantity

        # 3. Set completed timestamp + amount
        self.completed = db.func.now()
        self.amount = self.estimate()



class ProductOrder(db.Model):
    __tablename__ = "product_order"

    product_id = db.mapped_column(
        db.ForeignKey("products.id"), primary_key=True
    )
    order_id = db.mapped_column(
        db.ForeignKey("orders.id"), primary_key=True
    )

    quantity = db.mapped_column(db.Integer, nullable=False)

    product = db.relationship("Product")
    order = db.relationship("Order", back_populates="items")

    def line_total(self):
        return self.product.price * self.quantity
