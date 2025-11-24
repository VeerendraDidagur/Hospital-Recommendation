from flask import Flask, render_template, request, redirect, url_for
import requests
app = Flask(__name__)

RENDER_API_URL = "https://your-render-api.onrender.com/hospitals"


# ---------------------------------
# Home Route
# ---------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------
# Load hospitals + doctors from Render API
# ---------------------------------
@app.route("/book_appointment", methods=["GET"])
def book_appointment():
    try:
        params = {"city": "bangalore"}

        # Fetch data from render cloud backend
        response = requests.get(RENDER_API_URL, params=params, timeout=10)
        response.raise_for_status()

        hospitals = response.json()   # list of hospitals with doctors inside

    except Exception as e:
        print("Error fetching data:", e)
        hospitals = []

    return render_template("book_appointment.html", hospitals=hospitals)


# ---------------------------------
# After user picks hospital → load doctors dropdown
# ---------------------------------
@app.route("/get_doctors", methods=["POST"])
def get_doctors():
    hospital_id = request.form.get("hospital_id")

    # Call Render API again to get doctors for selected hospital
    try:
        response = requests.get(f"{RENDER_API_URL}/{hospital_id}")
        response.raise_for_status()
        hospital_data = response.json()

        doctors = hospital_data.get("doctors", [])

    except:
        doctors = []

    return render_template("select_doctor.html", doctors=doctors, hospital_id=hospital_id)


# ---------------------------------
# After selecting doctor + slot
# ---------------------------------
@app.route("/confirm_appointment", methods=["POST"])
def confirm_appointment():
    hospital_id = request.form.get("hospital_id")
    doctor_id = request.form.get("doctor_id")
    timeslot = request.form.get("timeslot")

    # You can store this in database later. For now show in success page.
    return render_template(
        "success.html",
        hospital_id=hospital_id,
        doctor_id=doctor_id,
        timeslot=timeslot
    )


# ---------------------------------
# Run server
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)
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
    h = next((x for x in hospitals if x["id"] == hid), None)

    doctor = {
        "name": request.form.get("name"),
        "image": request.form.get("image"),
        "specialties": request.form.get("specialties"),
        "experience": request.form.get("experience"),
        "rating": request.form.get("rating"),
        "qualification": request.form.get("qualification"),
    }

    # Sample clinic details (customizable per doctor later)
    clinic = {
        "name": h["name"],
        "fee": 700
    }

    return render_template(
        "book_appointment.html",
        doctor=doctor,
        clinic=clinic
    )
@app.route("/success")
def success():
    return render_template("success.html")

# -------------------------
# RUN
# -------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



























