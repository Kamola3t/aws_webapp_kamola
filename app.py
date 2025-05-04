from flask import Flask, request, render_template_string
import psycopg2

app = Flask(__name__)

# Connect to your PostgreSQL RDS
conn = psycopg2.connect(
    host="dbkamola.c32geugqgvkj.ap-southeast-1.rds.amazonaws.com",
    database="dbkamola",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Kamola App</title></head>
<body>
    <h1>Disney Movies Database</h1>
    <form action="/add" method="post">
        <input type="text" name="title" placeholder="Movie Title" required>
        <button type="submit">Add</button>
    </form>
    <form action="/delete" method="post">
        <input type="text" name="title" placeholder="Movie Title" required>
        <button type="submit">Delete</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/add", methods=["POST"])
def add_movie():
    title = request.form["title"]
    cur.execute("INSERT INTO tbl_kamola_disney_movies (title) VALUES (%s)", (title,))
    conn.commit()
    return "Movie added! <a href='/'>Go back</a>"

@app.route("/delete", methods=["POST"])
def delete_movie():
    title = request.form["title"]
    cur.execute("DELETE FROM tbl_kamola_disney_movies WHERE title = %s", (title,))
    conn.commit()
    return "Movie deleted! <a href='/'>Go back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
