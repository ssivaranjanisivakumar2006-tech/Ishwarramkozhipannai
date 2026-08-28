from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from dotenv import load_dotenv
import resend

load_dotenv()

app = Flask(__name__)

app.secret_key = "iswarram_kozhi_pannai_secret_key"

DATABASE = "farm.db"


# =========================
# RESEND SETUP
# =========================

resend.api_key = os.getenv("RESEND_API_KEY")

MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")


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


create_database()


# =========================
# SEND ORDER EMAIL
# =========================

def send_order_email(
    name,
    phone,
    product,
    quantity,
    address,
    order_type,
    message
):

    try:

        if not resend.api_key:
            print("RESEND_API_KEY is missing.")
            return False

        if not MAIL_RECEIVER:
            print("MAIL_RECEIVER is missing.")
            return False

        email_html = f"""
        <h2>🐔 NEW ORDER RECEIVED</h2>

        <hr>

        <p><b>Customer Name:</b> {name}</p>

        <p><b>Phone Number:</b> {phone}</p>

        <p><b>Product:</b> {product}</p>

        <p><b>Quantity:</b> {quantity}</p>

        <p><b>Address:</b> {address}</p>

        <p><b>Order Type:</b> {order_type}</p>

        <p><b>Customer Message:</b> {message}</p>

        <hr>

        <p><b>Iswarram Kozhi Pannai</b></p>
        """

        params = {
            "from": "onboarding@resend.dev",
            "to": [MAIL_RECEIVER],
            "subject": "🐔 New Order - Iswarram Kozhi Pannai",
            "html": email_html
        }

        response = resend.Emails.send(params)

        print("Resend Email Response:", response)

        return True

    except Exception as e:

        print("Resend Email Error:", e)

        return False


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
            # SAVE ORDER
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
            # SEND EMAIL
            # =========================

            email_sent = send_order_email(
                name,
                phone,
                product,
                quantity,
                address,
                order_type,
                message
            )


            if email_sent:

                flash(
                    "Order submitted successfully! "
                    "We received your order."
                )

            else:

                flash(
                    "Order submitted successfully! "
                    "We received your order, "
                    "but email notification could not be sent."
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