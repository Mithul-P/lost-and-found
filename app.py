from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import hashlib
import mysql.connector

# -----------------------------
# Flask Setup
# -----------------------------
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create upload folder if not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -----------------------------
# MySQL Database Setup (Clever Cloud)
# -----------------------------
db = mysql.connector.connect(
    host="bhe5ouni2ddurdorxrum-mysql.services.clever-cloud.com",
    user="urul80utrapmaxcl",
    password="YyU7mp07VLzS81iMc3Vr",  
    database="bhe5ouni2ddurdorxrum"
)
cursor = db.cursor()

# -----------------------------
# Utility Function: Image Hash
# -----------------------------
def get_image_hash(image_path):
    """Generate MD5 hash for an image file"""
    with open(image_path, "rb") as f:
        bytes = f.read()
        return hashlib.md5(bytes).hexdigest()

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lost', methods=['GET', 'POST'])
def lost():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(path)

            image_url = f"/{app.config['UPLOAD_FOLDER']}/{filename}"
            image_hash = get_image_hash(path)

            # Insert into database
            cursor.execute(
                "INSERT INTO items (name, description, image_url, image_hash) VALUES (%s, %s, %s, %s)",
                (name, description, image_url, image_hash)
            )
            db.commit()

            return render_template('success.html', message="Lost item uploaded successfully!")

    return render_template('lost.html')

@app.route('/found', methods=['GET', 'POST'])
def found():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(path)

            image_url = f"/{app.config['UPLOAD_FOLDER']}/{filename}"
            image_hash = get_image_hash(path)

            # Check for existing image hash
            cursor.execute("SELECT * FROM items WHERE image_hash = %s", (image_hash,))
            match = cursor.fetchone()

            if match:
                # Match found
                return render_template(
                    'match.html',
                    message="We found a possible match — is this your item?",
                    match=match
                )
            else:
                # Insert as a new found item
                cursor.execute(
                    "INSERT INTO items (name, description, image_url, image_hash) VALUES (%s, %s, %s, %s)",
                    (name, description, image_url, image_hash)
                )
                db.commit()
                return render_template('no_match.html', message="No matches found 😢")

        return redirect(url_for('index'))

    return render_template('found.html')

@app.route('/items')
def list_items():
    cursor.execute("SELECT * FROM items ORDER BY id DESC")
    items = cursor.fetchall()
    return render_template('items.html', items=items)

# -----------------------------
# Run
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
