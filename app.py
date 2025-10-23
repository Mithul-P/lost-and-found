from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER','static/uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.secret_key = os.getenv('SECRET_KEY','dev-secret')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST','127.0.0.1'),
        user=os.getenv('DB_USER','root'),
        password=os.getenv('DB_PASS',''),
        database=os.getenv('DB_NAME','lost_and_found'),
        port=int(os.getenv('DB_PORT',3306))
    )

ALLOWED = {'png','jpg','jpeg','gif'}

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.',1)[1].lower() in ALLOWED

@app.route('/')
def index():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM items ORDER BY created_at DESC LIMIT 12")
    items = cur.fetchall()
    cur.close()
    db.close()
    return render_template('index.html', items=items)

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        title = request.form.get('title','').strip()
        description = request.form.get('description','').strip()
        status = request.form.get('status','lost')
        location = request.form.get('location','').strip()
        event_date = request.form.get('event_date') or None
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        phone = request.form.get('phone','').strip()

        image_path = None
        file = request.files.get('image')
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(f"{int(datetime.utcnow().timestamp())}_{file.filename}")
                savepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(savepath)
                image_path = savepath
            else:
                flash('Invalid image type', 'danger')
                return redirect(request.url)

        db = get_db()
        cur = db.cursor()
        reporter_id = None
        if name or email or phone:
            cur.execute("INSERT INTO users (name,email,phone) VALUES (%s,%s,%s)", (name or None, email or None, phone or None))
            reporter_id = cur.lastrowid

        cur.execute("INSERT INTO items (title,description,category,status,location,event_date,image_path,reporter_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (title, description, None, status, location, event_date, image_path, reporter_id))
        db.commit()
        cur.close()
        db.close()
        flash('Item reported', 'success')
        return redirect(url_for('index'))
    return render_template('submit.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/items')
def list_items():
    q = request.args.get('q')
    sql = "SELECT * FROM items WHERE 1=1"
    params = []
    if q:
        like = f"%{q}%"
        sql += " AND (title LIKE %s OR description LIKE %s OR location LIKE %s)"
        params += [like, like, like]
    sql += " ORDER BY created_at DESC LIMIT 200"
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(sql, tuple(params))
    items = cur.fetchall()
    cur.close()
    db.close()
    return render_template('list.html', items=items, q=q)

@app.route('/item/<int:item_id>')
def view_item(item_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT i.*, u.name as reporter_name, u.email, u.phone FROM items i LEFT JOIN users u ON i.reporter_id = u.id WHERE i.id=%s", (item_id,))
    item = cur.fetchone()
    cur.close()
    db.close()
    if not item:
        flash('Item not found', 'warning')
        return redirect(url_for('index'))
    return render_template('view_item.html', item=item)

if __name__ == '__main__':
    print('Starting app on http://127.0.0.1:5000')
    app.run(debug=True)
