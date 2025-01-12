from flask import Flask, redirect
from flask import render_template, request
from flask_cors import CORS
import urllib
from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import json
import datetime
import base64
import cv2
import numpy as np
import re

global id_count
id_count = 1

load_dotenv()
client = OpenAI(
    api_key = os.getenv("HACKATHON_KEY")
)


def enhance_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    enhanced_img = cv2.merge((cl, a, b))
    return cv2.cvtColor(enhanced_img, cv2.COLOR_LAB2BGR)

def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def find_document_contour(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        if len(approx) == 4:
            return approx
    return None

def apply_perspective_transform(image, contour):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def process_image(image_path, end_path):
    image = cv2.imread(image_path)
    original = image.copy()
    
    edges = detect_edges(image)
    #cv2.imwrite("detect_edges.jpg", edges)
    
    contour = find_document_contour(edges)
    #contour_image = original.copy()
    #cv2.drawContours(contour_image, contour, -1, (0, 255, 0), 2)
    #cv2.imwrite("draw_contours.jpg", contour_image)

    if contour is None:
        print("No document found!")
        return
    
    scanned = apply_perspective_transform(original, contour)
    #cv2.imwrite("perspective_transform.jpg", scanned)
    
    #final = enhance_contrast(scanned)
    
    cv2.imwrite(end_path, scanned)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class PrescriptionInfo(BaseModel):
    id: int
    Name: str
    Strength: int
    StartDate: str
    Directions: str
    TimeOfDay: str
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

    global id_count

    image = request.files.get("image", "")
    if image:
        image.save("./raw.jpg")
    else:
        print("not sigma at ALL")
        print("***************** IMAGE NOT UPLOADED *****************")

    process_image("raw.jpg", "scanned.jpg")

    with open("scanned.jpg", "rb") as f:
        image_bytes = f.read()

    base64_image = base64.b64encode(image_bytes).decode('utf-8')

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
                        extract all 4 prescriptions and respond with json in the following format
                        {
                        "Name": "",  # name of drug
                        "Strength": 0,  # mg/pill
                        "StartDate": "", # start date (in format YYYYMMDD)
                        "Directions": "",  # just a string of directions
                        "TimeOfDay": "", # generate a suggestion if the user should take the medicine in the 'M' (morning) or 'E' (evening)
                        "Interval": 1,  # how often it should be taken (in days) (minimum 1)
                        "Quantity": 0,  # pills in bottle
                        "Refills": 0,  # number of refills
                        "EndDate": "",  # refill date if there are refills, if there are no refills then do StartDate(in format YYYYMMDD)
                        "Warnings": ""  # generate some warnings or side effects based on the medication
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

    prescription_info = response.choices[0].message.content
    match = re.search(r'```json (.*?)```', prescription_info, re.DOTALL)
    print(prescription_info)
    if match:
        prescription_info = match.group(1)

    print(prescription_info)
    if prescription_info[8] == '{':
        prescription_info = '[' + prescription_info[8:-4] + ']'
    else:
        prescription_info = prescription_info[8:-4]
    print(f"Perscription Info: {prescription_info}")
    dict_data = json.loads(prescription_info)

    # for each prescription in the image
    for i in range(len(dict_data)):
        data = dict_data[i]
        # logic to figure out what the end date is
        if data['StartDate'] == data['EndDate']:
            startdate = datetime.date(int(data['StartDate'][:4]), int(data['StartDate'][4:6]), int(data['StartDate'][6:8]))
            delta = datetime.timedelta(days=data['Quantity'] * data['Interval'])
            endDate = (startdate + delta).isoformat()
            endDate = endDate.replace("-", "")
            data['EndDate'] = endDate
        
        # adds the id count
        data['id'] = id_count
        id_count += 1

        # generates a time to take the medicine
        if data['TimeOfDay'] == 'M':
            data['Hour'] = "06"
        elif data['TimeOfDay'] == 'E':
            data['Hour'] = "18"
        else:
            data['Hour'] = "12"
        del data['TimeOfDay']

    print(f"DICT!!!!!!! {json.dumps(dict_data)}")
    return json.dumps(dict_data)
    

@app.route("/", methods=["GET"])
def getWelcome():
    return render_template('welcome.html')
@app.route("/app", methods=["GET"])
def getApp():
    return render_template('app.html')

##example perscription
prescription = {
    "id": 0, # number ID
    "Name": "Metformin",  # required
    "Strength": 500,  # required
    "StartDate": "20240102", # start date (in format YYYYMMDD) r
    "Directions": "Take 1 tablet by mouth up to 2 times daily",  # just a string of directions req
    "Hour": "09", # req
    "Interval": 3,  # how often it should be taken in days (minimum 1) req
    "Quantity": 0,  # pills in bottle   req
    "Refills": 0,  # number of refills  req
    "EndDate": "20240302",  # refill date if there are refills, end date if refills == 0 (in format YYYYMMDD) req
    "Warnings": "Take this medication with food"
}
@app.route('/create-event', methods=["POST"])
def create_event():
    prescription = request.get_json(force=True)
    if len(prescription["Hour"]) == 1:
        prescription["Hour"] = f"0{prescription['Hour']}"
    
    m_event_name = f"{prescription['Name']}+{prescription['Strength']}mg" #replace with drug name
    m_start_date_starttime = f"{prescription['StartDate']}T{prescription['Hour']}0000-0500"
    m_start_date_endtime = datetime.datetime.strptime(m_start_date_starttime, "%Y%m%dT%H%M%S%z") + datetime.timedelta(minutes=30)
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
    print(m_calendar_url)

    return m_calendar_url


def create_app():
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
