import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import mysql.connector
from PIL import Image
import imagehash
from dotenv import load_dotenv

# --------------------------
# Load environment variables
# --------------------------
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --------------------------
# DB Connection Helper
# --------------------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# --------------------------
# Routes
# --------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/lost', methods=['GET', 'POST'])
def lost():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            # Compute image hash
            hash_val = str(imagehash.average_hash(Image.open(image_path)))

            # Save to DB
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (name, description, image_url, image_hash) VALUES (%s, %s, %s, %s)",
                (name, description, image_path, hash_val)
            )
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/')

    return render_template('lost.html')


@app.route('/found', methods=['GET', 'POST'])
def found():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            # Compute hash of uploaded image
            hash_val = str(imagehash.average_hash(Image.open(image_path)))

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM items WHERE image_hash = %s", (hash_val,))
            match = cursor.fetchone()
            cursor.close()
            conn.close()

            if match:
                return f"<h2>Possible Match Found!</h2><p>Item Name: {match['name']}</p><p>Description: {match['description']}</p><img src='/{match['image_url']}' width='200'>"
            else:
                return "<h2>No match found yet. Please try again later.</h2>"

    return render_template('found.html')


if __name__ == '__main__':
    app.run(debug=True)
