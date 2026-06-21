import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
ALTER TABLE games
ADD COLUMN user_id INTEGER
""")
except:
    print("Column already exists")

cursor.execute("""
UPDATE games
SET user_id = 1
WHERE user_id IS NULL
""")

conn.commit()
conn.close()

print("Database upgraded")
