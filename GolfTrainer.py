import os, sqlite3

from flask import Flask, redirect, render_template, request, url_for
from openai import OpenAI
client = OpenAI(
    api_key = "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"
)

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        reflection = request.form["reflection"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.6,
            messages=[
                {"role": "system","content": "Golfers are going to provide you with an issue they are facing with their golf game. You need to provide them with some ways that they could go about fixing this problem and what they can work on. Try to avoid telling them to seek professional help or spend any money"},
                {"role": "user", "content": reflection}
            ]
        )
        msg = response.choices[0].message.content
        conn = get_db_connection()
        conn.execute("INSERT INTO prompts (reflection, msg) VALUES (?, ?)",
                     (reflection, msg))
        conn.commit()
        conn.close()
        return redirect(url_for("index", result=msg))

    result = request.args.get("result")
    return render_template("index.html", result=result)