from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

RANK_LIST = [
    "Iron 1", "Iron 2", "Iron 3",
    "Bronze 1", "Bronze 2", "Bronze 3",
    "Silver 1", "Silver 2", "Silver 3",
    "Gold 1", "Gold 2", "Gold 3",
    "Platinum 1", "Platinum 2", "Platinum 3",
    "Diamond 1", "Diamond 2", "Diamond 3",
    "Ascendant 1", "Ascendant 2", "Ascendant 3",
    "Immortal 1", "Immortal 2", "Immortal 3",
    "Radiant"
]

RANKS = {
    "Iron 1": 1,
    "Iron 2": 2,
    "Iron 3": 3,

    "Bronze 1": 4,
    "Bronze 2": 5,
    "Bronze 3": 6,

    "Silver 1": 7,
    "Silver 2": 8,
    "Silver 3": 9,

    "Gold 1": 10,
    "Gold 2": 11,
    "Gold 3": 12,

    "Platinum 1": 13,
    "Platinum 2": 14,
    "Platinum 3": 15,

    "Diamond 1": 16,
    "Diamond 2": 17,
    "Diamond 3": 18,

    "Ascendant 1": 19,
    "Ascendant 2": 20,
    "Ascendant 3": 21,

    "Immortal 1": 22,
    "Immortal 2": 23,
    "Immortal 3": 24,

    "Radiant": 25,
    
}

ROV_RANKS = {
    "Bronze": 1,
    "Silver": 2,
    "Gold": 3,
    "Platinum": 4,
    "Diamond": 5,
    "Conqueror": 6
}

app = Flask(__name__)
app.secret_key = "pet_secret_key"

@app.route("/")
def home():

    if "user" not in session or "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, game, value, goal, game_type FROM games WHERE user_id=?",
        (session["user_id"],)
    )

    games = cursor.fetchall()

    conn.close()

    game_data = []

    for game in games:

        current = game[2]
        goal = game[3]

        game_type = game[4]

        if game_type == "rank":

            if game[1] == "RoV":

                current_rank = ROV_RANKS.get(current, 1)
                goal_rank = ROV_RANKS.get(goal, 6)

            else:

                current_rank = RANKS.get(current, 1)
                goal_rank = RANKS.get(goal, 25)

            progress = int(
                (current_rank / goal_rank) * 100
            )

        else:

            try:

                current_level = int(current)
                goal_level = int(goal)

                progress = int(
                    (current_level / goal_level) * 100
                )

            except:

                progress = 0

        if progress > 100:
            progress = 100

        image = "default.png"

        if game[1].lower() == "valorant":
            image = "valorant.png"

        elif game[1].lower() == "rov":
            image = "rov.png"

        elif game[1].lower() == "line rangers":
            image = "linerangers.png"
        
        if game[1] == "Valorant":

            rank_image = current.lower().replace(" ", "") + ".png"

            if current == "Radiant":
                rank_image = "radiant.png"

        elif game[1] == "RoV":

            rank_image = "rov_default.png"

        else:

            rank_image = "level.png"

        goal_completed = False

        if progress >= 100:
            goal_completed = True

        game_data.append({
            "id": game[0],
            "game": game[1],
            "current": current,
            "goal": goal,
            "progress": progress,
            "image": image,
            "rank_image": rank_image,
            "game_type": game[4],
            "goal_completed": goal_completed,
        })

    total_games = len(game_data)

    if total_games > 0:
        avg_progress = sum(
            g["progress"] for g in game_data
        ) // total_games
    else:
        avg_progress = 0

    return render_template(
        "index.html",
        games=game_data,
        total_games=total_games,
        avg_progress=avg_progress
    )

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        new_game = request.form["game"]
        new_value = request.form["value"]
        new_goal = request.form["goal"]

        if new_game == "Valorant":
            new_game_type = "rank"

        elif new_game == "RoV":
            new_game_type = "rank"

        elif new_game == "Line Rangers":
            new_game_type = "level"

        else:
            new_game_type = "custom"

        cursor.execute(
            """
            UPDATE games
            SET game=?, value=?, goal=?, game_type=?
            WHERE id=?
            """,
            (
                new_game,
                new_value,
                new_goal,
                new_game_type,
                id
            )
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute(
        "SELECT id, game, value, goal FROM games WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )

    game = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        game=game,
        ranks=RANK_LIST
    )



@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        game = request.form["game"]
        value = request.form["value"]
        goal = request.form["goal"]

        if game == "Valorant":
            game_type = "rank"

        elif game == "RoV":
            game_type = "rank"

        elif game == "Line Rangers":
            game_type = "level"

        else:
            game_type = "custom"

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO games (game, value, goal, game_type, user_id) VALUES (?, ?, ?, ?, ?)",
            (game, value, goal, game_type, session["user_id"])
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM games WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            hashed_password = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()

        except:
            conn.close()
            return "Username already exists"

        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):

            session["user"] = username
            session["user_id"] = user[0]

            return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("user", None)
    session.pop("user_id", None)

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)