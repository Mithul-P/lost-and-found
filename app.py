from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# --- Database Configuration ---
# Use Clever Cloud environment variables (set in Render)
db_config = {
    'host': os.getenv('MYSQL_ADDON_HOST', 'bhe5ouni2ddurdorxrum-mysql.services.clever-cloud.com'),
    'user': os.getenv('MYSQL_ADDON_USER', 'urul80utrapmaxcl'),
    'password': os.getenv('MYSQL_ADDON_PASSWORD', 'YyU7mp07VLzS81iMc3Vr'),
    'database': os.getenv('MYSQL_ADDON_DB', 'bhe5ouni2ddurdorxrum'),
    'port': int(os.getenv('MYSQL_ADDON_PORT',3306))
}

# --- Database Connection ---
try:
    conn = mysql.connector.connect(**db_config)
    print("✅ Database connected successfully.")
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
    conn = None


# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        if not conn or not conn.is_connected():
            return "Database not connected", 500

        name = request.form.get('name')
        description = request.form.get('description')
        location = request.form.get('location')
        contact = request.form.get('contact')

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description, location, contact) VALUES (%s, %s, %s, %s)",
            (name, description, location, contact)
        )
        conn.commit()
        cursor.close()

        return redirect(url_for('list_items'))

    return render_template('submit.html')


@app.route('/items')
def list_items():
    if not conn or not conn.is_connected():
        return "Database not connected", 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items ORDER BY id DESC")
    items = cursor.fetchall()
    cursor.close()

    return render_template('list.html', items=items)


@app.route('/item/<int:item_id>')
def view_item(item_id):
    if not conn or not conn.is_connected():
        return "Database not connected", 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()

    if not item:
        return "Item not found", 404

    return render_template('view_item.html', item=item)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
