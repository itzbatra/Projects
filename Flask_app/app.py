from flask import Flask, render_template, redirect, url_for, abort
from pathlib import Path
from db import db
from models import Product, Category, Customer, Order

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///My.db"
app.instance_path = Path(".").resolve()

db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/products")
def products_list():
    stmt = db.select(Product).order_by(Product.name)
    products = db.session.execute(stmt).scalars()
    return render_template("products.html", products=products)


@app.route("/categories")
def categories_list():
    stmt = db.select(Category).order_by(Category.name)
    categories = db.session.execute(stmt).scalars()
    return render_template("categories.html", categories=categories)


@app.route("/categories/<string:name>")
def category_detail(name):
    stmt = db.select(Category).where(Category.name == name)
    category = db.session.execute(stmt).scalar()
    if not category:
        return render_template("error.html", message="Category not found"), 404
    return render_template("category_detail.html", category=category)


@app.route("/customers")
def customers_list():
    stmt = db.select(Customer).order_by(Customer.name)
    customers = db.session.execute(stmt).scalars()
    return render_template("customers.html", customers=customers)


@app.route("/customers/<int:id>")
def customer_detail(id):
    stmt = db.select(Customer).where(Customer.id == id)
    customer = db.session.execute(stmt).scalar()
    if not customer:
        return render_template("error.html", message="Customer not found"), 404
    return render_template("customer_detail.html", customer=customer)


@app.route("/orders")
def orders_list():
    stmt = db.select(Order).order_by(Order.created.desc())
    orders = db.session.execute(stmt).scalars()
    return render_template("orders.html", orders=orders)


@app.route("/orders/<int:id>")
def order_detail(id):
    o = db.session.get(Order, id)
    if not o:
        return render_template("error.html", message="Order not found"), 404
    return render_template("order.html", order=o)


@app.route("/orders/<int:id>/complete", methods=["POST"])
def complete_order(id):
    o = db.session.get(Order, id)
    if not o:
        return render_template("error.html", message="Order not found"), 404
    try:
        o.complete()
        db.session.add(o)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return render_template("error.html", message=str(e)), 409
    return redirect(url_for("order_detail", id=id))


if __name__ == "__main__":
    app.run(debug=True, port=8888)
