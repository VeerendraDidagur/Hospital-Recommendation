from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy hospital dataset (without pandas)
hospitals = [
    {"name": "City Hospital", "location": "Mumbai", "rating": 4.5},
    {"name": "Green Valley Hospital", "location": "Delhi", "rating": 4.2},
    {"name": "Sunrise Medical Center", "location": "Bangalore", "rating": 4.7,"contact no:9108497662,Dr Name:Santosh"},
    {"name": "National Care Hospital", "location": "Hyderabad", "rating": 4.4},
]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        city = request.form.get("city").lower()
        for hospital in hospitals:
            if hospital["location"].lower() == city:
                results.append(hospital)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

