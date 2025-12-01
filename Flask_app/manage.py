import csv
import random
from datetime import datetime as dt, timedelta

from app import app
from db import db
from models import Product, Category, Customer, Order, ProductOrder


def drop_tables():
    db.Model.metadata.drop_all(bind=db.engine)
    print("Dropped all tables")


def create_tables():
    db.Model.metadata.create_all(bind=db.engine)
    print("Tables created")


def import_data():
    with open("products.csv", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cat_name = row["category"]

            category = db.session.execute(
                db.select(Category).where(Category.name == cat_name)
            ).scalar()

            if not category:
                category = Category(name=cat_name)
                db.session.add(category)
                db.session.commit()

            product = Product(
                name=row["name"],
                price=float(row["price"]),
                inventory=int(row["available"]),
                category=category
            )

            db.session.add(product)

        db.session.commit()
        print("Products imported")


def import_customers():
    with open("customers.csv", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            customer = Customer(
                name=row["name"],
                phone=row["phone"],
                email=row["email"]
            )
            db.session.add(customer)

        db.session.commit()
        print("Customers imported")


def generate_random_orders(n=5):
    for _ in range(n):
        random_customer = db.session.execute(
            db.select(Customer).order_by(db.func.random())
        ).scalar()

        if not random_customer:
            print("No customers found")
            return

        created_at = dt.now() - timedelta(
            days=random.randint(1, 3),
            hours=random.randint(0, 15),
            minutes=random.randint(0, 45)
        )

        order = Order(customer=random_customer, created=created_at)
        db.session.add(order)

        num_products = random.randint(3, 6)
        products = db.session.execute(
            db.select(Product)
            .order_by(db.func.random())
            .limit(num_products)
        ).scalars()

        for prod in products:
            quantity = random.randint(1, 5)
            p = ProductOrder(
                product=prod,
                order=order,
                quantity=quantity
            )
            db.session.add(p)

    db.session.commit()
    print(f"Generated {n} random orders.")


if __name__ == "__main__":
    import sys

    with app.app_context():

        if "reset" in sys.argv:
            drop_tables()
            create_tables()
            import_data()
            import_customers()
            print("Database reset complete.")

        if "orders" in sys.argv:
            generate_random_orders(10)

        if len(sys.argv) == 1:
            drop_tables()
            create_tables()
            import_data()
            import_customers()
            generate_random_orders(10)
            print("Database initialized with sample data.")
