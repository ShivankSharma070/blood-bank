import json
import os
from pathlib import Path
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

DATA_FILE = Path(os.getenv("DATA_FILE", "data/donors.json"))
GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Blood Bank V1</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f4; }
        .box { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
        input, select, button { padding: 10px; margin: 5px; }
        button { background: #c62828; color: white; border: none; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background: #c62828; color: white; }
    </style>
</head>
<body>
    <h1>Blood Bank Management System - V1</h1>

    <div class="box">
        <h2>Add Donor</h2>

        <form action="/add" method="POST">
            <input name="name" placeholder="Donor Name" required>

            <select name="blood_group" required>
                {% for group in groups %}
                    <option value="{{ group }}">{{ group }}</option>
                {% endfor %}
            </select>

            <input name="phone" placeholder="Phone Number" required>
            <input name="city" placeholder="City" required>

            <button type="submit">Add Donor</button>
        </form>
    </div>

    <div class="box">
        <h2>Donor Records</h2>

        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Blood Group</th>
                <th>Phone</th>
                <th>City</th>
            </tr>

            {% for donor in donors %}
            <tr>
                <td>{{ donor["id"] }}</td>
                <td>{{ donor["name"] }}</td>
                <td>{{ donor["blood_group"] }}</td>
                <td>{{ donor["phone"] }}</td>
                <td>{{ donor["city"] }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5">No donors registered yet.</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

def load_donors():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]")

    return json.loads(DATA_FILE.read_text())

def save_donors(donors):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(donors, indent=4))

@app.route("/")
def home():
    return render_template_string(
        PAGE,
        donors=load_donors(),
        groups=GROUPS
    )

@app.route("/add", methods=["POST"])
def add_donor():
    donors = load_donors()

    donor = {
        "id": max((d["id"] for d in donors), default=0) + 1,
        "name": request.form["name"].strip(),
        "blood_group": request.form["blood_group"],
        "phone": request.form["phone"].strip(),
        "city": request.form["city"].strip()
    }

    donors.append(donor)
    save_donors(donors)

    return redirect("/")

if __name__ == "__main__":
    load_donors()
    app.run(host="0.0.0.0", port=5000)
