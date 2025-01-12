from flask import Flask, redirect
from flask import render_template, request
from flask_cors import CORS
from datetime import datetime, timedelta
import urllib
from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import json
import datetime
import base64


# load_dotenv()
# client = OpenAI(
#     api_key = os.getenv("HACKATHON_KEY")
# )

# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

class PrescriptionInfo(BaseModel):
    id: int
    Name: str
    Strength: int
    StartDate: str
    Directions: str
    Hour: str
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

    # file_content = image.read()
    # base64_image = base64.b64encode(file_content).decode('utf-8')

    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": 
    #                     """
    #                     extract the prescription  and respond with json in the following format
    #                     {
    #                     "id": 0, # number ID
    #                     "Name": "",  # name of drug
    #                     "Strength": 0,  # mg/pill
    #                     "StartDate": "", # start date (in format YYYYMMDD)
    #                     "Directions": "",  # just a string of directions
    #                     "Hour": 01, # time of day (in hours 00-24) that is best to take this
    #                     "Interval": 1,  # how often it should be taken (in days) (minimum 1)
    #                     "Quantity": 0,  # pills in bottle
    #                     "Refills": 0,  # number of refills
    #                     "EndDate": "",  # refill date if there are refills, if there are no refills then  (in format YYYYMMDD)
    #                     "Warnings": ""  # any warnings or side effects
    #                     }
    #                     """,
    #                 },
    #                 {
    #                     "type": "image_url",
    #                     "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
    #                 },
    #             ],
    #         }
    #     ],
    # )
    # prescription_info = response.choices[0].message.content
    # dict_data = json.loads(prescription_info[7:-3])

    # for i in range(0, len(dict_data)):
    #     if dict_data[i]['StartDate'] == dict_data[i]['EndDate']:
    #         startdate = datetime.date(int(dict_data[i]['StartDate'][:4]), int(dict_data[i]['StartDate'][4:6]), int(dict_data[i]['StartDate'][6:8]))
    #         delta = datetime.timedelta(days=dict_data[i]['Quantity'] * dict_data[i]['Interval'])
    #         endDate = (startdate + delta).isoformat()
    #         endDate = endDate.replace("-", "")
    #         dict_data[i]['EndDate'] = endDate

    # return json.dumps(dict_data)
    

@app.route("/", methods=["GET"])
def getWelcome():
    return render_template('welcome.html')
@app.route("/app", methods=["GET"])
def getApp():
    return render_template('app.html')

##example perscription
prescription = {
    "id": 0, # number ID
    "Name": "Metformin",  # name of drug
    "Strength": 500,  # mg/pill
    "StartDate": "20240102", # start date (in format YYYYMMDD)
    "Directions": "Take 1 tablet by mouth up to 2 times daily",  # just a string of directions
    "Hour": "09",
    "Interval": 3,  # how often it should be taken in days (minimum 1)
    "Quantity": 0,  # pills in bottle   
    "Refills": 0,  # number of refills
    "EndDate": "20240302",  # refill date if there are refills, end date if refills == 0 (in format YYYYMMDD)
    "Warnings": "Take this medication with food"
}
@app.route('/create-event')
def create_event():
    prescription = request.get("prescription")
    m_event_name = f"{prescription['Name']} {prescription['Strength']}mg" #replace with drug name
    m_start_date_starttime = f"{prescription['StartDate']}T{prescription['Hour']}0000-0500"
    m_start_date_endtime = datetime.strptime(m_start_date_starttime, "%Y%m%dT%H%M%S%z") + timedelta(minutes=30)
    m_start_date_endtime = m_start_date_endtime.strftime("%Y%m%dT%H%M%S%z")  # Convert to string
    m_end_date = f"{prescription['EndDate']}T000000Z"
    m_interval = prescription['Interval']
    #description
    m_recurrence = f"RRULE:FREQ=DAILY;INTERVAL={m_interval};UNTIL={m_end_date}"
    m_description = f"DIRECTIONS:\n{prescription['Directions']}\n\nWARNINGS:\n{prescription['Warnings']}" #add Warnings + frequency here
    m_encoded_description = urllib.parse.quote(m_description)
    
    
    
    # make url
    m_calendar_url = (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text={m_event_name}"
        f"&dates={m_start_date_starttime}/{m_start_date_endtime}"
        f"&details={m_encoded_description}"
        f"&recur={m_recurrence}"
    )
    # calendar_url = "https://calendar.google.com/calendar/u/0/r/eventedit?text=Metformin+500mg&dates=20240101T090000-0500/20240102T093000-0500&details=DIRECTIONS:%0ATake+1+tablet+by+mouth+up+to+2+times+daily%0A%0AWARNINGS:%0ATake+this+medication+with+food&recur=RRULE:FREQ%3DDAILY;INTERVAL%3D1;UNTIL%3D20110201T020000Z"
    # print(calendar_url)

    return redirect(m_calendar_url)

def create_app():
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
