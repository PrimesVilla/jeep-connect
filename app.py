from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)
JSON_FILE = './static/Routes.json'

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    return render_template("map.html")  # Make sure 'index.html' is in the 'templates' folder

@app.route("/edit")
def edit():
    return render_template("test.html") 

# Load JSON data
def load_data():
    with open(JSON_FILE, "r") as file:
        return json.load(file)

# Save JSON data
def save_data(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Read JSON
@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(load_data())

# Add new entry
@app.route("/data", methods=["POST"])
def update_or_add_data():
    new_entry = request.json
    data = load_data()

    # Check if the route already exists based on a unique identifier
    for i, route in enumerate(data):
        if route.get("X1") == new_entry.get("X1"):  # Assuming each route has a unique "id"
            data[i] = new_entry  # Update the existing route
            save_data(data)
            return jsonify({"message": "Route updated", "data": new_entry})
        
    data.append(new_entry)# If not found, append as new route
    save_data(data)
    return jsonify({"message": "New route added", "data": new_entry})


if __name__ == "__main__":
    app.run(debug=True)
