import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS serial_numbers (
    id INTEGER PRIMARY KEY,
    serial TEXT NOT NULL UNIQUE
)
''')

conn.commit()
conn.close()
