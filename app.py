from flask import Flask, render_template, request, g, redirect, url_for, session
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    serial_number = request.form['serial_number']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM serial_numbers WHERE serial = ?', (serial_number,))
    result = cursor.fetchone()
    
    if result:
        return "Serial number already registered."
    else:
        cursor.execute('INSERT INTO serial_numbers (serial) VALUES (?)', (serial_number,))
        db.commit()
        return "Serial number registered successfully."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'your_admin_password':  # Replace with your desired password
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Invalid password"
    return render_template('login.html')

@app.route('/logout')
