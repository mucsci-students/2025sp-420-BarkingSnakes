from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('./flask.html')

@app.route("/classlist")
def classlist():
    return jsonify(["Car", "Racecar", "Spaceship", "School"])

@app.route("/relationlist")
def relationlist():
    return jsonify(["Car -> Racecar", "Racecar -> Spaceship", "Spaceship -> School"])

@app.route("/classdetails")
def classdetails():
    class_name = request.args.get('name')
    # Replace this with actual logic to fetch class details
    class_info = {
        "Car": {
            "fields": ["make", "model", "year"],
            "methods": ["drive()", "stop()"]
        },
        "Racecar": {
            "fields": ["make", "model", "year", "top_speed"],
            "methods": ["drive()", "stop()", "race()"]
        },
        "Spaceship": {
            "fields": ["name", "crew_size", "destination"],
            "methods": ["launch()", "land()"]
        },
        "School": {
            "fields": ["name", "location", "num_students"],
            "methods": ["enroll_student()", "graduate_student()"]
        }
    }
    details = class_info.get(class_name, {"fields": [], "methods": []})
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True)