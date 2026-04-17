from flask import Flask, render_template
import json
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

LOG_FILE = "logs.json"


def load_logs():
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


@app.route("/")
def dashboard():
    logs = load_logs()
    total_attacks = len(logs)
    top_attacker = "None"

    if logs:
        counts = {}
        for log in logs:
            ip = log["ip"]
            counts[ip] = counts.get(ip, 0) + 1
        top_attacker = max(counts, key=counts.get)

    return render_template(
        "index.html",
        logs=logs[-10:],
        total_attacks=total_attacks,
        top_attacker=top_attacker,
    )


@app.route("/logs")
def all_logs():
    logs = load_logs()
    return render_template("logs.html", logs=logs)


@app.route("/alerts")
def alerts():
    logs = load_logs()
    suspicious = [log for log in logs if log["attempts"] >= 3]
    return render_template("alerts.html", alerts=suspicious)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)