from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -----------------------------
# Sample hospital + doctors data (now includes "features")
# -----------------------------
hospitals = [
    {
        "id": "h1",
        "name": "City Hospital",
        "location": "Bangalore",
        "address": "City Hospital Rd, Bangalore, Karnataka",
        "rating": 4.6,
        "specialists": ["Cardiologist", "Neurologist", "ENT", "General Physician", "Dermatologist"],
        "symptoms": ["COVID", "Stomach Pain", "Headache", "Cold and Cough", "Fever", "Constipation"],
        "doctors": [
            {
                "name": "Dr. Rahul Sharma",
                "specialties": ["Fever", "Cold and Cough", "General Physician"],
                "experience": 12,
                "rating": 4.8,
                "qualification": "MBBS, MD",
                "image": "https://i.pravatar.cc/150?img=68"
            },
            {
                "name": "Dr. Sneha Kapoor",
                "specialties": ["COVID", "Headache", "Pulmonology"],
                "experience": 9,
                "rating": 4.6,
                "qualification": "MBBS, DM",
                "image": "https://i.pravatar.cc/150?img=32"
            }
        ],
        "features": {
            "blood": {
                "groups": ["B+", "B-", "O+", "O-", "AB+", "AB-"],
                "units": {"B+": 12, "B-": 6, "O+": 25, "O-": 10, "AB+": 4, "AB-": 2},
                "emergency_contact": "+91 98765 43210"
            },
            "organ": {
                "organs_available": ["Kidney", "Liver", "Heart", "Lungs", "Eyes"],
                "waiting_list": "1 Kidney, 2 Hearts",
                "contact": "+91 91234 56780"
            },
            "icu": {
                "icu_vacant": 7,
                "normal_beds": 4,
                "ventilators": 5
            },
            "emergency": {
                "ambulance_24x7": 3,
                "waiting_time": "15 minutes"
            }
        }
    },
    {
        "id": "h2",
        "name": "East Point Hospital",
        "location": "East Point Hospital, Cheemasandra, Bengaluru",
        "address": "3P39+M3 Bengaluru, Karnataka 560049",
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
                "image": "https://i.pravatar.cc/150?img=65"
            },
            {
                "name": "Dr. Mayank Patil",
                "specialties": ["Fever", "Dentist", "General Physician"],
                "experience": 12,
                "rating": 4.8,
                "qualification": "MBBS, MD",
                "image": "https://i.pravatar.cc/150?img=68"
            },
            {
                "name": "Dr. Neha Varma",
                "specialties": ["Dentist", "Tooth Pain"],
                "experience": 7,
                "rating": 4.5,
                "qualification": "BDS, MDS",
                "image": "https://i.pravatar.cc/150?img=5"
            },
        ],
        "features": {
            "blood": {
                "groups": ["A+", "A-", "O+", "O-"],
                "units": {"A+": 8, "A-": 3, "O+": 20, "O-": 7},
                "emergency_contact": "+91 99876 54321"
            },
            "organ": {
                "organs_available": ["Kidney", "Liver", "Eyes"],
                "waiting_list": "2 Kidney, 0 Hearts",
                "contact": "+91 90123 45678"
            },
            "icu": {
                "icu_vacant": 5,
                "normal_beds": 6,
                "ventilators": 4
            },
            "emergency": {
                "ambulance_24x7": 2,
                "waiting_time": "20 minutes"
            }
        }
    },
    {
        "id": "h3",
        "name": "M S Ramaiah Hospital",
        "location": "Bangalore",
        "address": "MSR Hospital Rd, Bengaluru, Karnataka",
        "rating": 4.7,
        "specialists": ["Cardiologist", "Neurologist", "ENT", "General Physician", "Dermatologist"],
        "symptoms": ["COVID", "Stomach Pain", "Headache", "Cold and Cough", "Fever", "Constipation"],
        "doctors": [],
        "features": {
            "blood": {
                "groups": ["B+", "O+", "AB+"],
                "units": {"B+": 5, "O+": 10, "AB+": 1},
                "emergency_contact": "+91 90000 11111"
            },
            "organ": {
                "organs_available": ["Kidney", "Liver"],
                "waiting_list": "3 Kidney, 1 Heart",
                "contact": "+91 90000 22222"
            },
            "icu": {
                "icu_vacant": 3,
                "normal_beds": 8,
                "ventilators": 2
            },
            "emergency": {
                "ambulance_24x7": 4,
                "waiting_time": "10 minutes"
            }
        }
    },
]


# ---------------------------------
# ROUTES
# ---------------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("city", "")
        results = [h for h in hospitals if city.lower() in h["location"].lower()]
        return render_template("index.html", hospitals=results, city=city)
    return render_template("index.html")


@app.route("/hospital/<hid>")
def hospital_detail(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        return "Hospital not found", 404
    # pass a google maps link to template (template will urlencode)
    maps_link = f"https://www.google.com/maps/search/?api=1&query={h['address']}"
    return render_template("hospital.html", hospital=h, maps_link=maps_link)


@app.route('/choose_doctor')
def choose_doctor():
    speciality = request.args.get('speciality')
    hid = request.args.get('hid')
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        return "Hospital not found", 404
    matched_doctors = [d for d in h["doctors"] if any(speciality.lower() in sp.lower() for sp in d["specialties"])]
    return render_template("doctors.html", hospital=h, doctors=matched_doctors, speciality=speciality)


@app.route('/choose_symptom')
def choose_symptom():
    symptom = request.args.get('symptom')
    hid = request.args.get('hid')
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        return "Hospital not found", 404
    matched_doctors = [d for d in h["doctors"] if any(symptom.lower() in sp.lower() for sp in d["specialties"])]
    return render_template("doctors.html", hospital=h, doctors=matched_doctors, speciality=symptom)


@app.route("/hospital/<hid>/book", methods=["POST"])
def book_doctor(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        return "Hospital not found", 404

    doctor = {
        "name": request.form.get("name"),
        "image": request.form.get("image"),
        "specialties": request.form.get("specialties"),
        "experience": request.form.get("experience"),
        "rating": request.form.get("rating"),
        "qualification": request.form.get("qualification"),
    }

    clinic = {"name": h["name"], "fee": 700}

    return render_template("book_appointment.html", doctor=doctor, clinic=clinic, hospital=h)


@app.route("/hospital/<hid>/features")
def hospital_features(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        return "Hospital not found", 404
    return render_template("features.html", hospital=h)


@app.route("/success")
def success():
    return render_template("success.html")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
