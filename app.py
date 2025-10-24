from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# --- Get database credentials from environment variables ---
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "lost_and_found")
DB_PORT = int(os.environ.get("DB_PORT", 3306))

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    contact = request.form['contact']
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, description, contact) VALUES (%s, %s, %s)", (name, description, contact))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('list_items'))


@app.route('/list')
def list_items():
    conn = get_db_connection()
    items = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('list.html', items=items)


@app.route('/view/<int:item_id>')
def view_item(item_id):
    conn = get_db_connection()
    item = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
    return render_template('view_item.html', item=item)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
