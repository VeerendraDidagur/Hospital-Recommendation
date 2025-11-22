from flask import Flask, render_template, request, redirect, url_for, flash
import uuid
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL

app = Flask(__name__)
app.secret_key = "change_this_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    specialization = db.Column(db.String(200))
    cost_category = db.Column(db.Integer)
    rating = db.Column(db.Float)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    results = Hospital.query.all()

        if request.method == 'POST':
        city = request.form.get('city')
        if not city or city == "":
        return render_template("index.html", error="Please enter a city")

        hospitals = Hospital.query.filter_by(city=city).all()
        return render_template("index.html", hospitals=hospitals)

    return render_template("index.html")
        query = Hospital.query
        if city:
            query = query.filter(Hospital.city.ilike(city))
        if specialization:
            query = query.filter(Hospital.specialization.ilike(f"%{specialization}%"))
        if max_cost:
            query = query.filter(Hospital.cost_category <= int(max_cost))
        if min_rating:
            query = query.filter(Hospital.rating >= float(min_rating))

        results = query.all()

    return render_template("index.html", results=results)

@app.route("/hospital/<int:hid>")
def hospital_detail(hid):
    h = Hospital.query.get(hid)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))

    plan = {
        "title": "Develop m-Health Applications",
        "steps": [
            {"label": "Design the app architecture", "desc": "Build Android/iOS mobile app connected to centralized DB."},
            {"label": "Integrate APIs & GIS", "desc": "Government data + Maps APIs for routing & location."},
            {"label": "Key Features", "desc": "Login, health profile, search/filter, booking & emergency routing."},
            {"label": "Security", "desc": "Authentication + encryption + HIPAA/GDPR compliance."},
        ],
    }
    return render_template("hospital.html", hospital=h, plan=plan)

@app.route("/hospital/<int:hid>/book", methods=["POST"])
def book_appointment(hid):
    h = Hospital.query.get(hid)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))

    name = request.form.get("name")
    phone = request.form.get("phone")
    dt = request.form.get("datetime")

    new_appt = Appointment(
        patient_name=name,
        phone=phone,
        datetime=dt,
        hospital_id=hid,
        status="Pending"
    )
    db.session.add(new_appt)
    db.session.commit()

    flash("Appointment submitted successfully! Hospital will contact you.", "success")
    return redirect(url_for("hospital_detail", hid=hid))

    flash(f"Appointment requested at {h.name} for {name} on {datetime}. Booking ID: {booking_id}", "success")
    return redirect(url_for("hospital_detail", hid=hid))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), nullable=False)
    datetime = db.Column(db.String(100))

    user = db.relationship("User", backref="appointments")
    hospital = db.relationship("Hospital", backref="appointments")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
with app.app_context():
    db.drop_all()
    db.create_all()








