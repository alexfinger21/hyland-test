import os
from flask import Flask
from flask import render_template, request
from flask_cors import CORS
import openai

app = Flask(__name__,
                  static_url_path="",
                  static_folder="web/static",
                  template_folder="web/templates",
            )

# /
# /prescriptions

# uploading images to backend
UPLOAD_FOLDER = "web/uploads"
@app.route("/upload-photo", methods=["POST"])
def upload_file():
    image = request.files.get("image", "")
    if image:
        print("File uploaded successfully")
    else:
        return
    
    # return render_template("upload.html")
    return ""

# rendering html
@app.route("/", methods=["GET"])
def getTemplate():
    return render_template('template.html', title="Templates Page", message="Welcome to the Templates Page!")

@app.route("/", methods=["GET"])
def sendPrescription():
    pass

prescription = {
    "#": 0, # number ID
    "Name": "",  # name of drug
    "Strength": 0,  # mg/pill
    "Start Date": "", # start date (in format YYYYMMDD)
    "Directions": "",  # just a string of directions
    "Time": 0, # best time in hour from 0-24 to take this medication
    "Interval": "",  # how often it should be taken in days (minimum 1)
    "Quantity": "",  # pills in bottle
    "Refills": "",  # number of refills
    "End Date": "",  # refill date if there are refills, end date if refills == 0 (in format YYYYMMDD)
    "Warnings": ""  # any warnings
}





# run
def create_app():
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
