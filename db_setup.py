import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')  # Create or connect to SQLite database
    cursor = conn.cursor()
    
    # Read schema and execute
    with open('schema.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    
    conn.commit()
    conn.close()
    print("Database and table created successfully.")

if __name__ == "__main__":
    create_database()