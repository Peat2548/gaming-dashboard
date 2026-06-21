import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE games
    ADD COLUMN goal TEXT
    """)
except:
    print("goal already exists")

cursor.execute("""
UPDATE games
SET goal='Not Set'
WHERE goal IS NULL
""")

conn.commit()
conn.close()

print("Done")