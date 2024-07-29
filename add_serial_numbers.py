import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# List of serial numbers to add
serial_numbers = [
    'SN123456',
    'SN123457',
    'SN123458',
    'SN123459',
    'SN123460'
]

# Insert serial numbers into the database
for serial in serial_numbers:
    try:
        cursor.execute('INSERT INTO serial_numbers (serial) VALUES (?)', (serial,))
        print(f"Serial number {serial} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Serial number {serial} already exists in the database.")

# Commit the changes and close the connection
conn.commit()
conn.close()
