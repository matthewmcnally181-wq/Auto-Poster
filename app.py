from flask import Flask, render_template, request, redirect, session, jsonify
import os
import uuid

app = Flask(__name__)
app.secret_key = "secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

users = {}

# ---------------- AUTH ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username not in users:
            users[username] = {"password": password, "platforms": {}}

        if users[username]["password"] == password:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- CONNECT ----------------

@app.route("/connect", methods=["POST"])
def connect():
    user = session["user"]
    platform = request.form["platform"]

    users[user]["platforms"][platform] = "CONNECTED"
    return redirect("/dashboard")


# ---------------- UPLOAD ----------------

@app.route("/upload", methods=["POST"])
def upload():
    user = session["user"]
    file = request.files["video"]

    filename = str(uuid.uuid4()) + "_" + file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    return jsonify({"path": path})


# ---------------- POST ----------------

@app.route("/post", methods=["POST"])
def post_video():
    data = request.json
    platforms = data["platforms"]

    results = []
    for p in platforms:
        results.append(f"Posted to {p} (simulated)")

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)