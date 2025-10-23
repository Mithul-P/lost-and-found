from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure MySQL connection
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "lost_and_found"),
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        contact = request.form['contact']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO items (name, description, category, contact) VALUES (%s, %s, %s, %s)",
                (name, description, category, contact),
            )
            connection.commit()
            cursor.close()
            connection.close()
            flash("Item added successfully!", "success")
            return redirect(url_for('show_items'))
        else:
            flash("Database connection failed.", "danger")
    return render_template('add_item.html')

@app.route('/items')
def show_items():
    connection = get_db_connection()
    items = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items ORDER BY id DESC")
        items = cursor.fetchall()
        cursor.close()
        connection.close()
    return render_template('show_items.html', items=items)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q', '')
    results = []
    if query:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM items WHERE name LIKE %s OR description LIKE %s", (f"%{query}%", f"%{query}%"))
            results = cursor.fetchall()
            cursor.close()
            connection.close()
    return render_template('search.html', results=results, query=query)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
