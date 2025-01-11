from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import json
import base64

# load_dotenv()
# client = OpenAI(
#     api_key = os.getenv("HACKATHON_KEY")
# )

# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# class PerscriptionInfo(BaseModel):
#     id: int
#     Name: str
#     Strength: int
#     StartDate: str
#     Directions: str
#     Time: int
#     Interval: str
#     Quantity: int
#     Refills: int
#     EndDate: str
#     Warnings: str




# image_path = "p1.jpg"
# base64_image = encode_image(image_path)

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
#                     "Time": 0, # time of day (in hours 0-24) that is best to take this
#                     "Interval": "",  # how often it should be taken (in days) (minimum 1)
#                     "Quantity": 0,  # pills in bottle
#                     "Refills": 0,  # number of refills
#                     "EndDate": "",  # refill date if there are refills, end date if refills = 0 (in format YYYYMMDD)
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

# event = response.choices[0].message.parsed
# print(event)

# json_string = json.dumps(event, indent=4)
# print(json_string)
# print(event)

