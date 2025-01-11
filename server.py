from flask import Flask
from flask import render_template, request
from flask_cors import CORS

from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import base64


load_dotenv()
client = OpenAI(
    api_key = os.getenv("HACKATHON_KEY")
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class PrescriptionInfo(BaseModel):
    id: int
    Name: str
    Strength: int
    StartDate: str
    Directions: str
    Time: int
    Interval: int
    Quantity: int
    Refills: int
    EndDate: str
    Warnings: str



app = Flask(
    __name__,
    static_url_path="",
    static_folder="web/static",
    template_folder="web/templates",
)

@app.route("/upload-photo", methods=["POST"])
def process_photo():
    image = request.files.get("image", "")
    image.save("./test.jpg")

    file_content = image.read()
    base64_image = base64.b64encode(file_content).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": 
                        """
                        extract the prescription  and respond with json in the following format
                        {
                        "id": 0, # number ID
                        "Name": "",  # name of drug
                        "Strength": 0,  # mg/pill
                        "StartDate": "", # start date (in format YYYYMMDD)
                        "Directions": "",  # just a string of directions
                        "Time": 0, # time of day (in hours 0-24) that is best to take this
                        "Interval": 1,  # how often it should be taken (in days) (minimum 1)
                        "Quantity": 0,  # pills in bottle
                        "Refills": 0,  # number of refills
                        "EndDate": "",  # refill date if there are refills, end date if refills = 0 (in format YYYYMMDD)
                        "Warnings": ""  # any warnings or side effects
                        }
                        """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    perscription_info = response.choices[0].message.content
    return perscription_info
    

@app.route("/", methods=["GET"])
def getWelcome():
    return render_template('welcome.html')
@app.route("/app", methods=["GET"])
def getApp():
    return render_template('app.html')

def create_app():
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
