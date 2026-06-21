import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE games
    ADD COLUMN game_type TEXT
    """)
except:
    print("Column already exists")

cursor.execute("""
UPDATE games
SET game_type='rank'
WHERE game_type IS NULL
""")

conn.commit()
conn.close()

print("Done")