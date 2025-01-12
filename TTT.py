import json
prescription_info = '''```json
{
    "Name": "Alprazolam",
    "Strength": 0.5,
    "StartDate": "20231209",
    "Directions": "Take 1 tablet by mouth up to 3 times daily",
    "TimeOfDay": "M",
    "Interval": 1,
    "Quantity": 90,
    "Refills": 0,
    "EndDate": "20231209",
    "Warnings": "This drug may impair the ability to drive or operate machinery. Use care until you become familiar with its effects."
}
```'''
if prescription_info[8] == '{':

    prescription_info = '[' + prescription_info[8:-4] + ']'
else:
    prescription_info = prescription_info[8:-4]
    # try:
    #     dict_data = json.loads(prescription_info[7:-3])
    # except:
    #     return json.dumps({"error": "incorrect image"})
# dict_data = json.loads(prescription_info[7:-3])
# print(dict_data)
print(prescription_info)
