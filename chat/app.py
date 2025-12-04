from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "stock_update_key"  # required for flash messages

# -----------------------------
# Sample hospital + doctors data (includes "features")
# -----------------------------
hospitals = [
    {
        "id": "h1",
        "name": "City Hospital",
        "location": "25/91 20th Main Road, Rajajinagar, Bengaluru, Karnataka 560010",
        "address": "XHW2+6C Bengaluru, Karnataka",
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
    # ... other hospitals unchanged (h2..h5) ...
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
    maps_link = f"https://www.google.com/maps/search/?api=1&query={h['address']}"
    return render_template("hospital.html", hospital=h, maps_link=maps_link)


@app.route('/choose_doctor')
def choose_doctor():
    speciality = request.args.get('speciality', '')
    hid = request.args.get('hid')
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        return "Hospital not found", 404
    matched_doctors = [d for d in h["doctors"] if any(speciality.lower() in sp.lower() for sp in d["specialties"])]
    return render_template("doctors.html", hospital=h, doctors=matched_doctors, speciality=speciality)


@app.route('/choose_symptom')
def choose_symptom():
    symptom = request.args.get('symptom', '')
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


# -------------------------
# BOOK BLOOD
# -------------------------
@app.route("/book_blood/<hid>", methods=["POST"])
def book_blood(hid):
    hospital = next((h for h in hospitals if h["id"] == hid), None)
    if not hospital:
        flash("Hospital not found")
        return redirect(url_for('hospital_features', hid=hid))

    group = (request.form.get("blood_group") or "").strip()
    try:
        qty = int(request.form.get("quantity", 0))
    except (ValueError, TypeError):
        flash("Enter a valid quantity")
        return redirect(url_for('hospital_features', hid=hid))

    units = hospital["features"]["blood"]["units"]

    # validation
    if group == "" or group not in units:
        flash("Enter a valid function")
        return redirect(url_for('hospital_features', hid=hid))

    if qty <= 0:
        flash("Enter a valid quantity")
        return redirect(url_for('hospital_features', hid=hid))

    if units[group] < qty:
        flash("Not enough quantity available")
        return redirect(url_for('hospital_features', hid=hid))

    # update
    units[group] -= qty

    # if group becomes zero, remove from units dict and groups list
    if units[group] == 0:
        del units[group]
        groups_list = hospital["features"]["blood"].get("groups", [])
        if group in groups_list:
            groups_list.remove(group)

    flash("Booked Successfully ✔")
    return redirect(url_for('hospital_features', hid=hid))


# -------------------------
# BOOK ORGAN
# -------------------------
@app.route("/book_organ/<hid>", methods=["POST"])
def book_organ(hid):
    hospital = next((h for h in hospitals if h["id"] == hid), None)
    if not hospital:
        flash("Hospital not found")
        return redirect(url_for('hospital_features', hid=hid))

    organ = (request.form.get("organ_name") or "").strip()
    try:
        qty = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        flash("Enter a valid quantity")
        return redirect(url_for('hospital_features', hid=hid))

    available_list = hospital["features"]["organ"].get("organs_available", [])

    # validation: organ must exist in list
    if organ == "" or organ not in available_list:
        flash("Enter a valid function")
        return redirect(url_for('hospital_features', hid=hid))

    # For organs we assume booking reserves the organ(s) and we remove it if booked.
    # If you later want counts for organs, change structure to a dict similar to blood units.
    # Here we accept qty and remove the organ if qty >=1 (single organ items)
    # (You could extend this later)
    # remove organ from available list
    for _ in range(qty):
        if organ in available_list:
            available_list.remove(organ)

    flash("Booked Successfully ✔")
    return redirect(url_for('hospital_features', hid=hid))


# -------------------------
# BOOK ICU / VENTILATOR
# -------------------------
@app.route("/book_icu/<hid>", methods=["POST"])
def book_icu(hid):
    hospital = next((h for h in hospitals if h["id"] == hid), None)
    if not hospital:
        flash("Hospital not found")
        return redirect(url_for('hospital_features', hid=hid))

    icu_type_raw = (request.form.get("icu_type") or "").strip().lower()
    try:
        qty = int(request.form.get("quantity", 0))
    except (ValueError, TypeError):
        flash("Enter a valid quantity")
        return redirect(url_for('hospital_features', hid=hid))

    # map friendly names to internal keys
    mapping = {
        "icu": "icu_vacant",
        "icu bed": "icu_vacant",
        "normal": "normal_beds",
        "normal bed": "normal_beds",
        "ventilator": "ventilators",
        "ventilators": "ventilators"
    }

    key = mapping.get(icu_type_raw)
    if not key:
        flash("Enter a valid function")
        return redirect(url_for('hospital_features', hid=hid))

    if qty <= 0:
        flash("Enter a valid quantity")
        return redirect(url_for('hospital_features', hid=hid))

    available = hospital["features"]["icu"].get(key, 0)
    if available < qty:
        flash("Not enough quantity available")
        return redirect(url_for('hospital_features', hid=hid))

    hospital["features"]["icu"][key] = available - qty
    flash("Booked Successfully ✔")
    return redirect(url_for('hospital_features', hid=hid))


@app.route("/success")
def success():
    return render_template("success.html")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
