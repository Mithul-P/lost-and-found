from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this for production

# MySQL Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "lostandfound")
    )

# ---------------------------
# ROUTES
# ---------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        location = request.form['location']
        contact = request.form['contact']

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO items (item_name, description, location, contact) VALUES (%s, %s, %s, %s)",
                (item_name, description, location, contact)
            )
            db.commit()
            cursor.close()
            db.close()
            flash("Item added successfully!", "success")
        except Exception as e:
            flash(f"Database error: {e}", "danger")

        return redirect(url_for('show_items'))
    return render_template('add_item.html')


@app.route('/items')
def show_items():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items ORDER BY id DESC")
        items = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('items.html', items=items)
    except Exception as e:
        flash(f"Database connection failed: {e}", "danger")
        return render_template('items.html', items=[])


@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM items WHERE item_name LIKE %s OR description LIKE %s",
                (f"%{keyword}%", f"%{keyword}%")
            )
            results = cursor.fetchall()
            cursor.close()
            db.close()
        except Exception as e:
            flash(f"Search error: {e}", "danger")
    return render_template('search.html', results=results)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
