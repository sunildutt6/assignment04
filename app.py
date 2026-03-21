from flask import Flask, render_template, request, redirect, url_for,jsonify
from config import Config
from db import (
    get_all_categories,
    get_all_products,
    get_product_by_id,
    insert_category,
    insert_product,
    get_single_user
)

app = Flask(__name__)
app.config.from_object(Config)

#register page
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/check-username")
def check_username():
    username = request.args.get("username", "").strip()

    if username== "":
        return jsonify({
            "available":False,
            "message": "Username required"
        })
    taken_usernames = ["admin", "sharif", "sunil", "khalid" , "newuser123"]

    if username.lower() in taken_usernames:
        return jsonify({
            "available": False,
            "message": "Username is already taken"
        })

    return jsonify({
        "available":True,
        "message":""
    })


@app.route("/")
def index():
    user = get_single_user()
    return render_template("index.html", user=user)

@app.route("/products")
def products_list():
    products = get_all_products()
    return render_template("products.html", products=products)

@app.route("/product/<int:product_id>")
def show_product(product_id):
    product = get_product_by_id(product_id)

    if product:
        return render_template("show_product.html", product=product)
    return "Product Not Found", 404

@app.route("/add-category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if not name:
            return "Category name required"

        insert_category(name)
        return redirect(url_for("products_list"))

    return render_template("add_category.html")

@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = request.form.get("price", "").strip()
        stock = request.form.get("stock", "").strip()
        categoryId = request.form.get("categoryId", "").strip()

        if not name or not price or not stock or not categoryId:
            return "All fields are required"

        if float(price) <= 0:
            return "Price must be positive"

        if int(stock) < 0:
            return "Stock cannot be negative"

        insert_product(name, price, stock, categoryId)
        return redirect(url_for("products_list"))

    categories = get_all_categories()
    return render_template("add_product.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)