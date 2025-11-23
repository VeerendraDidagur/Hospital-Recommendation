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
                "image": "doctors/dr1.jpg"
            },
            {
                "name": "Dr. Sneha Kapoor",
                "specialties": ["COVID", "Headache", "Pulmonology"],
                "experience": 9,
                "rating": 4.6,
                "qualification": "MBBS, DM",
                "image": "doctors/dr2.jpg"
            }
        ]
    },
    {
        "id": "h2",
        "name": "East Point Hospital",
        "location": "Bangalore",
        "address": "3P93+M3 Bengaluru,Karnataka",
        "rating": 4.5,
        "specialists": ["Orthopedic", "Dentist", "Cardiologist", "ENT"],
        "symptoms": ["Chest Pain", "Headache", "Skin Allergy", "Joint Pain"],
        "doctors": [
            {
                "name": "Dr. Ramesh Kumar",
                "specialties": ["Joint Pain", "Orthopedics"],
                "experience": 15,
                "rating": 4.9,
                "qualification": "MBBS, MS Ortho",
                "image": "VectorStock.com/53211461"
            },
            {
                "name": "Dr. Neha Varma",
                "specialties": ["Dentist", "Tooth Pain"],
                "experience": 7,
                "rating": 4.5,
                "qualification": "BDS, MDS",
                "image": "doctors/dr2.jpg"
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
    if not h:
        return "Hospital not found", 404
    return render_template("hospital.html", hospital=h)

@app.route("/choose/<hid>", methods=["GET", "POST"])
def choose(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    return render_template("choose.html", hospital=h)

@app.route('/choose_symptom')
def choose_symptom():
    symptom = request.args.get('symptom')
    hid = request.args.get('hid')

    # Find hospital by ID
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        return "Hospital not found", 404

    # Filter doctors based on symptom → doctor.specialties list
    matched_doctors = []
    for d in h["doctors"]:
        if any(symptom.lower() in s.lower() for s in d["specialties"]):
            matched_doctors.append(d)

    return render_template(
        "doctors.html",
        hospital=h,
        doctors=matched_doctors,
        speciality=symptom    # same variable used in doctors.html
    )

@app.route('/choose_doctor')
def choose_doctor():
    speciality = request.args.get('speciality')
    hid = request.args.get('hid')

    # find hospital by ID
    h = next((x for x in hospitals if x["id"] == hid), None)

    if not h:
        return "Hospital not found", 404

    # filter doctors within that hospital
    matched_doctors = []
    for d in h["doctors"]:
        if any(speciality.lower() in sp.lower() for sp in d["specialties"]):
            matched_doctors.append(d)

    return render_template(
        "doctors.html",
        hospital=h,
        doctors=matched_doctors,
        speciality=speciality
    )

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














