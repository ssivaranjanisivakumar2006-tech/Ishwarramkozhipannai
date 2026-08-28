from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = "iswarram_kozhi_pannai_secret_key"

DATABASE = "farm.db"


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# CREATE DATABASE
# =========================

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


# Create database when application starts
create_database()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# PRODUCTS
# =========================

@app.route("/products")
def products():
    return render_template("products.html")


# =========================
# SERVICES
# =========================

@app.route("/services")
def services():
    return render_template("services.html")


# =========================
# GALLERY
# =========================

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# =========================
# ORDER
# =========================

@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        try:

            name = request.form.get("name", "").strip()
            phone = request.form.get("phone", "").strip()
            product = request.form.get("product", "").strip()
            quantity = request.form.get("quantity", "").strip()
            address = request.form.get("address", "").strip()
            order_type = request.form.get("order_type", "").strip()
            message = request.form.get("message", "").strip()

            # Check required fields
            if not all([
                name,
                phone,
                product,
                quantity,
                address,
                order_type
            ]):

                flash("Please fill in all required fields.")

                return redirect(url_for("order"))


            # =========================
            # SAVE ORDER TO DATABASE
            # =========================

            conn = get_db_connection()

            conn.execute("""
                INSERT INTO orders
                (
                    name,
                    phone,
                    product,
                    quantity,
                    address,
                    order_type,
                    message
                )
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


            # =========================
            # SUCCESS MESSAGE
            # =========================

            flash(
                "Order submitted successfully! "
                "We received your order."
            )

            return redirect(url_for("order"))


        except Exception as e:

            print("ORDER ERROR:", e)

            flash(
                "Something went wrong. "
                "Please try again."
            )

            return redirect(url_for("order"))


    return render_template("order.html")


# =========================
# CONTACT
# =========================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )