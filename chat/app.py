from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -----------------------------
# Sample hospital + doctors data
# -----------------------------
hospitals = [
    {
        "id": "h1",
        "name": "City Hospital",
        "location": "Bangalore",
        "specialists": ["Cardiologist", "Neurologist", "ENT", "General Physician", "Dermatologist"],
        "symptoms": ["COVID", "Stomach Pain", "Headache", "Cold and Cough", "Fever", "Constipation"],
        "doctors": [
            {
                "name": "Dr. Rahul Sharma",
                "specialties": ["Fever", "Cold and Cough", "General Physician"],
                "experience": 12,
                "rating": 4.8,
                "qualification": "MBBS, MD",
                "image": "https://i.pravatar.cc/150?img=12"
            },
            {
                "name": "Dr. Sneha Kapoor",
                "specialties": ["COVID", "Headache", "Pulmonology"],
                "experience": 9,
                "rating": 4.6,
                "qualification": "MBBS, DM",
                "image": "https://i.pravatar.cc/150?img=25"
            }
        ]
    },
    {
        "id": "h2",
        "name": "East Point Hospital",
        "location": "Bangalore",
        "specialists": ["Orthopedic", "Dentist", "Cardiologist", "ENT"],
        "symptoms": ["Chest Pain", "Headache", "Skin Allergy", "Joint Pain"],
        "doctors": [
            {
                "name": "Dr. Ramesh Kumar",
                "specialties": ["Joint Pain", "Orthopedics"],
                "experience": 15,
                "rating": 4.9,
                "qualification": "MBBS, MS Ortho",
                "image": "https://i.pravatar.cc/150?img=5"
            },
            {
                "name": "Dr. Neha Varma",
                "specialties": ["Dentist", "Tooth Pain"],
                "experience": 7,
                "rating": 4.5,
                "qualification": "BDS, MDS",
                "image": "https://i.pravatar.cc/150?img=32"
            },
        ]
    }
]

# ---------------------------------
# ROUTES
# ---------------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("city")
        results = [h for h in hospitals if city.lower() in h["location"].lower()]
        return render_template("index.html", hospitals=results, city=city)
    return render_template("index.html")

@app.route("/hospital/<hid>")
def hospital_detail(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    return render_template("hospital.html", hospital=h)

@app.route("/choose/<hid>", methods=["GET", "POST"])
def choose(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    return render_template("choose.html", hospital=h)

@app.route("/doctors/<hid>", methods=["POST"])
def doctors(hid):
    symptom = request.form.get("symptom")
    h = next((x for x in hospitals if x["id"] == hid), None)

    # filter doctors matching selected symptom
    match = []
    for d in h["doctors"]:
        if symptom in d["specialties"]:
            match.append(d)

    return render_template("doctors.html", hospital=h, doctors=match, symptom=symptom)

@app.route("/hospital/<hid>/book", methods=["POST"])
def book_doctor(hid):
    doctor_name = request.form.get("name")
    h = next((x for x in hospitals if x["id"] == hid), None)

    return render_template("success.html", doctor=doctor_name, hospital=h["name"])
# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)




