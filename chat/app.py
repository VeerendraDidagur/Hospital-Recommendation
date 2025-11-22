from flask import Flask, render_template, request, redirect, url_for, flash
import uuid
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL


app = Flask(__name__)

app.secret_key = "change_this_secret"  # use env var in prod

# Simple in-memory dataset (replace with DB in production)
hospitals = [
    {"id": "h1", "name": "City Hospital", "location": "Mumbai", "rating": 4.5, "address":"123 MG Road, Mumbai"},
    {"id": "h2", "name": "Green Valley Hospital", "location": "Delhi", "rating": 4.2, "address":"45 Connaught Place, Delhi"},
    {"id": "h3", "name": "Sunrise Medical Center", "location": "Bangalore", "rating": 4.7, "address":"88 MG Road, Bangalore"},
    {"id": "h4", "name": "East Point Hospital", "location": "Bangalore", "rating": 4.8, "address":"3P39+M3 Bengaluru,Karnataka"},
    {"id": "h5", "name": "H Nanjappa Hospital", "location": "Bangalore", "rating": 4.9, "address":"Malleshwaram, Bangalore"},
    {"id": "h6", "name": "V Care Hospital", "location": "Bangalore", "rating": 4.4, "address":"K R Puram, Bangalore"},
    {"id": "h7", "name": "National Care Hospital", "location": "Hyderabad", "rating": 4.4, "address":"12 Banjara Hills, Hyderabad"},
]



# Home/search page
@app.route("/", methods=["GET", "POST"])
def index():
    results = hospitals
    if request.method == "POST":
        city = request.form.get("city", "").strip().lower()
        results = [h for h in hospitals if h["location"].lower() == city]
    return render_template("index.html", results=results)

# Hospital detail page
@app.route("/hospital/<int:hid>")
def hospital_detail(hid):
    hospital = Hospital.query.get(hid)
    if not hospital:
        flash("Hospital not found", "error")
        return redirect(url_for("home"))

    return render_template("hospital.html", hospital=hospital)


# Simple appointment booking endpoint (demo)
@app.route("/hospital/<hid>/book", methods=["POST"])
def book_appointment(hid):
    h = next((x for x in hospitals if x["id"] == hid), None)
    if not h:
        flash("Hospital not found", "error")
        return redirect(url_for("index"))

    # In real app: validate user auth, store booking to DB, send confirmation, etc.
    name = request.form.get("name", "Anonymous")
    phone = request.form.get("phone", "")
    datetime = request.form.get("datetime", "")
    # Fake booking id:
    booking_id = str(uuid.uuid4())[:8]
    # For demo we just flash success:
    flash(f"Appointment requested at {h['name']} for {name} on {datetime}. Booking ID: {booking_id}", "success")
    return redirect(url_for("hospital_detail", hid=hid))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    specialization = db.Column(db.String(200))
    cost_category = db.Column(db.Integer)  # 1=Low, 2=Medium, 3=High
    rating = db.Column(db.Float)
    # NEW FIELDS
    specialists = db.Column(db.ARRAY(db.String))    # Example: ["Cardiology","Neurology","Orthopedics"]
    symptoms = db.Column(db.ARRAY(db.String))       # Example: ["Fever","Headache","Joint Pain","Cough"]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200), nullable=False)
with app.app_context():
    db.create_all()

with app.app_context():
    east_point = Hospital(
        name="East Point Hospital",
        address="3P39+M3 Bengaluru, Karnataka",
        city="Bangalore",
        rating=4.8,
        specialization="Multi-specialty",
        cost_category=2,
        specialists=["Cardiology", "Neurology", "Orthopedics", "Dermatology"],
        symptoms=["Chest Pain", "Headache", "Skin Allergy", "Joint Pain"]
    )
    db.session.add(east_point)
    db.session.commit()
    print("Hospital added successfully!")










