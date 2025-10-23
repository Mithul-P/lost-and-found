from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this to any random string

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return conn
    except Error as e:
        print(f"Database connection failed: {e}")
        return None


# ---------- ROUTES ----------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Item added successfully!", "success")
    else:
        flash("Database connection failed.", "error")

    return redirect(url_for('index'))


@app.route('/items')
def show_items():
    conn = get_db_connection()
    items = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('items.html', items=items)


# ---------- RENDER ENTRY POINT ----------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
