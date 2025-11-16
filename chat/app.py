from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Sample hospital dataset (You can replace with real data)
data = pd.DataFrame([
    {"name": "City Hospital", "location": "Bangalore", "rating": 4.5, "speciality": "Cardiology"},
    {"name": "Global Health Care", "location": "Hyderabad", "rating": 4.2, "speciality": "Neurology"},
    {"name": "Apollo Hospital", "location": "Chennai", "rating": 4.8, "speciality": "Orthopedics"},
    {"name": "AIIMS Hospital", "location": "Delhi", "rating": 4.9, "speciality": "General"},
    {"name": "Manipal Hospital", "location": "Bangalore", "rating": 4.7, "speciality": "Cardiology"}
])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    location = request.form.get("location").lower()
    speciality = request.form.get("speciality").lower()

    results = data[
        (data["location"].str.lower().str.contains(location)) &
        (data["speciality"].str.lower().str.contains(speciality))
    ]

    return render_template("result.html", hospitals=results.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
