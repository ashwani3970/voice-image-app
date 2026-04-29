from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import difflib

app = Flask(__name__)

IMAGE_FOLDER = os.path.join("static", "images")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").upper().replace(" ", "")

    image_files = [f.split(".")[0] for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    # Get top 3 matches
    matches = difflib.get_close_matches(query, image_files, n=3, cutoff=0.4)

    results = []

    for match in matches:
        for file in os.listdir(IMAGE_FOLDER):
            if file.startswith(match):
                results.append(file)

    return jsonify({"results": results})

@app.route("/image/<filename>")
def image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)