from flask import Flask, render_template, request
from mashup import create_mashup
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form["singer"]
        videos = int(request.form["videos"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        try:
            create_mashup(singer, videos, duration, email)
            return "Mashup generated and emailed successfully"
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
