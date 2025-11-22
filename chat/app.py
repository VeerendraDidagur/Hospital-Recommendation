from flask import Flask, render_template, request, redirect, url_for, flash
import uuid

app = Flask(__name__)
app.secret_key = "change_this_secret"

# -------------------------
# Hospital dummy data
# -------------------------
hospitals = [
    {
        "id": "h1",
        "name": "City Hospital",
        "location": "Mumbai",
        "rating": 4.5,
        "address": "123 MG Road, Mumbai",
        "specialists": ["Cardiologist", "Neurologist", "Orthopedic", "Dermatologist"],
        "symptoms": ["Chest Pain", "Headache", "Skin Allergy", "Joint Pain"]
    },
    {
        "id": "h2",
        "name": "Green Valley Hospital",
        "location": "Delhi",
        "rating": 4.2,
        "address": "45 Connaught Place, Delhi",
        "specialists": ["Cardiologist", "Urologist", "ENT", "Pediatrician"],
        "symptoms": ["Fever", "Cough", "Ear Pain", "Abdominal Pain"]
    },
    {
        "id": "h3",
        "name": "Sunrise Medical Center",
        "location": "Bangalore",
        "rating": 4.7,
        "address": "88 MG Road, Bangalore",
        "specialists": ["Oncologist", "General Physician", "Orthopedic", "Psychiatrist"],
        "symptoms": ["Fatigue", "Back Pain", "Anxiety", "Neck Pain"]
    },
    {
        "id": "h4",
        "name": "National Care Hospital",
        "location": "Hyderabad",
        "rating": 4.4,
        "address": "12 Banjara Hills, Hyderabad",
        "specialists": ["Cardiologist", "Neurologist", "Pulmonologist", "Gastroenterologist"],
        "symptoms": ["Breathing Issues", "Vomiting", "Dizziness", "Chest Pain"]
    }
]

# -------------------------
# HOME & SEARCH
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    results = hospitals
    if request.method == "POST":
        city = request.form.get("city", "").strip().lower()
        results = [h for h in hospitals if h["location"].lower() == city]
    return render_template("index.html", results=results)

# -------------------------
# HOSPITAL DETAILS
# -------------------------
@app.route("/hospital/<hid>")
def hospital_detail(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))
    return render_template("hospital.html", hospital=h)

# -------------------------
# NEW PAGE — SELECT SPECIALIST / SYMPTOM
# -------------------------
@app.route("/hospital/<hid>/choose")
def choose_option(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))
    return render_template("choose.html", hospital=h)

# -------------------------
# RESULT AFTER SELECTING OPTION
# -------------------------
@app.route("/hospital/<hid>/result", methods=["POST"])
def hospital_result(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))

    selected_specialist = request.form.get("specialist")
    selected_symptom = request.form.get("symptom")

    msg = ""
    if selected_specialist:
        msg = f"Based on your selection, we recommend booking an appointment with a **{selected_specialist}** specialist."
    elif selected_symptom:
        msg = f"Your symptom '{selected_symptom}' is commonly treated here. Doctors are available for further diagnosis."

    return render_template("result.html", hospital=h, message=msg)

# -------------------------
# APPOINTMENT BOOKING
# -------------------------
@app.route("/hospital/<hid>/book", methods=["POST"])
def book_appointment(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))

    name = request.form.get("name", "Anonymous")
    phone = request.form.get("phone", "")
    datetime = request.form.get("datetime", "")
    booking_id = str(uuid.uuid4())[:8]

    flash(f"Appointment booked at {h['name']} for {name} on {datetime}. Booking ID: {booking_id}", "success")
    return redirect(url_for("hospital_detail", hid=hid))
    
@app.route("/hospital/<hid>/choose")
def choose_category(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))

    return render_template("choose.html", hospital=h)
    

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

