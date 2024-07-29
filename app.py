from flask import Flask, request, redirect, url_for, render_template, session, g
import sqlite3
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
DATABASE = '/tmp/database.db'  # Adjust path as needed

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def get_db():
    """Connect to the SQLite database."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(DATABASE)
    return g.sqlite_db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection."""
    db = getattr(g, 'sqlite_db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    """Customer homepage."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if request.method == 'POST':
        if request.form['password'] == 'your_admin_password':  # Replace with your desired password
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Invalid password", 403
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and end the session."""
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    """Admin page for adding and searching serial numbers."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/add_serials', methods=['POST'])
def add_serials():
    """Add serial numbers to the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    serial_numbers = request.form['serial_numbers'].split()
    db = get_db()
    cursor = db.cursor()
    for serial in serial_numbers:
        try:
            cursor.execute('INSERT INTO serial_numbers (serial) VALUES (?)', (serial,))
        except sqlite3.IntegrityError:
            pass
    db.commit()
    return redirect(url_for('admin'))

@app.route('/search_serials', methods=['GET'])
def search_serials():
    """Search for serial numbers in the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    query = request.args.get('query', '')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM serial_numbers WHERE serial LIKE ?', (f'%{query}%',))
    results = cursor.fetchall()
    return render_template('search_results.html', results=results, query=query)

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle and log exceptions."""
    app.logger.error(f"Exception occurred: {e}", exc_info=True)
    return "An internal error occurred. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
