str1 = '''
```json
{
  "Name": "Amoxicillin",
  "Strength": 500,
  "Interval": 1,
  "Quantity": 21,
  "Refills": 0,
  "EndDate": "19901203",
  "Warnings": "Possible side effects include nausea, diarrhea, and allergic reactions. Consult a healthcare provider if side effects occur."
}
```
'''

str2 = '''
```json
[
    {
        "Name": "Medrol dosepak",
        "Strength": 0,
        "StartDate": "20150313",
        "Directions": "Take as directed on pak until gone",
        "TimeOfDay": "M",
        "Interval": 1,
        "Quantity": 1,
        "Refills": 0,
        "EndDate": "20150313",
        "Warnings": "May cause side effects such as increased appetite, mood changes, and difficulty sleeping."
    },
    {
        "Name": "Clindamycin",
        "Strength": 300,
        "StartDate": "20150313",
        "Directions": "Take 1 cap TID until gone",
        "TimeOfDay": "M",
        "Interval": 1,
        "Quantity": 21,
        "Refills": 0,
        "EndDate": "20150313",
        "Warnings": "Possible side effects include diarrhea, nausea, and potential allergic reactions."
    },
    {
        "Name": "Peridex",
        "Strength": 0,
        "StartDate": "20150313",
        "Directions": "Take capful swish for 1 min and expectorate",
        "TimeOfDay": "M",
        "Interval": 1,
        "Quantity": 1,
        "Refills": 1,
        "EndDate": "20150313",
        "Warnings": "Can cause mouth irritation and changes in taste."
    }
]
```
'''

print(str2[9])

#print(json_str[8:-4])