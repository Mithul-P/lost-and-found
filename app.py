from flask import Flask, render_template, request
import mysql.connector
from PIL import Image
import imagehash
import os

app = Flask(__name__)

# ==========================
# Database connection setup
# ==========================
def get_connection():
    conn = mysql.connector.connect(
        host="bhe5ouni2ddurdorxrum-mysql.services.clever-cloud.com",
        user="urul80utrapmaxcl",
        password="YyU7mp07VLzS81iMc3Vr",
        database="bhe5ouni2ddurdorxrum"
    )
    return conn

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# ==========================
# LOST ITEM ROUTE
# ==========================
@app.route('/lost', methods=['GET', 'POST'])
def lost():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        file = request.files['image']

        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            # Compute image hash
            img = Image.open(image_path)
            image_hash = str(imagehash.average_hash(img))
            image_url = f"/{image_path}"

            # Reconnect to DB safely
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO items (name, description, image_url, image_hash) VALUES (%s, %s, %s, %s)",
                (name, description, image_url, image_hash)
            )
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('message.html', msg="Lost item added successfully!")
    return render_template('lost.html')

# ==========================
# FOUND ITEM ROUTE
# ==========================
@app.route('/found', methods=['GET', 'POST'])
def found():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        file = request.files['image']

        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            img = Image.open(image_path)
            image_hash = str(imagehash.average_hash(img))
            image_url = f"/{image_path}"

            conn = get_connection()
            cursor = conn.cursor()

            # Try to match with lost items
            cursor.execute("SELECT name, description, image_url FROM items WHERE image_hash = %s", (image_hash,))
            match = cursor.fetchone()

            if match:
                msg = f"Possible match found! Lost item: {match[0]} - {match[1]}"
            else:
                msg = "No match found. Item added to found list."
                cursor.execute(
                    "INSERT INTO items (name, description, image_url, image_hash) VALUES (%s, %s, %s, %s)",
                    (name, description, image_url, image_hash)
                )
                conn.commit()

            cursor.close()
            conn.close()
            return render_template('message.html', msg=msg)
    return render_template('found.html')


if __name__ == '__main__':
    app.run(debug=True)
