from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "iswarram_kozhi_pannai_secret_key"

DATABASE = "farm.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity TEXT NOT NULL,
            address TEXT NOT NULL,
            order_type TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        product = request.form["product"]
        quantity = request.form["quantity"]
        address = request.form["address"]
        order_type = request.form["order_type"]
        message = request.form["message"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO orders
            (name, phone, product, quantity, address, order_type, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            product,
            quantity,
            address,
            order_type,
            message
        ))

        conn.commit()
        conn.close()

        flash("Your order request has been submitted successfully!")

        return redirect(url_for("order"))

    return render_template("order.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)