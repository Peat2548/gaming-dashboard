import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game TEXT,
    value TEXT
)
""")

cursor.execute("DELETE FROM games")

cursor.execute("""
INSERT INTO games (game, value)
VALUES
('Valorant', 'Immortal 3'),
('RoV', 'Conqueror'),
('Line Rangers', '300')
""")

conn.commit()
conn.close()

print("Database Ready")