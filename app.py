from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=True)
