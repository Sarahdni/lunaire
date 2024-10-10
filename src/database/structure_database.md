Modification 1:

{
  "database": "LUNAIRE",
  "collections": {
    "users": [
      {
        "_id": ObjectId(),
        "email": "string",
        "name": "string",
        "age": "string",
        "country": "string",
        "cycle_info": {
          "last_period_date": ISODate(),
          "period_duration": "number",
          "cycle_length": "number"
        },
        "calendar_info": {
          "calendar_type": "string",
          "calendar_url": "string"
        },
        "created_at": ISODate(),
        "updated_at": ISODate()
      }
    ]
  }
}



modification 2:

{
  "_id": {
    "$oid": "6707b585c7755d9e2a482763"
  },
  "personal_info": {
    "email": "sarahdni89@gmail.com",
    "name": "sartia",
    "age": "30's",
    "country": "Italy",
    "language": "fr"
  },
  "cycle_info": {
    "last_period_date": {
      "$date": "2024-10-02T00:00:00.000Z"
    },
    "period_duration": 4,
    "cycle_length": 28,
    "cycle_history": []
  },
  "calendar_info": {
    "calendar_type": "ical",
    "calendar_url": "file:///Users/sarahdinari/Desktop/Lunaire/sartia_calendar_12months.ics",
    "last_generated": {
      "$date": "2024-10-10T11:12:22.280Z"
    }
  },
  "preferences": {
    "notifications": true
  },
  "created_at": {
    "$date": "2024-10-10T11:07:49.098Z"
  },
  "updated_at": {
    "$date": "2024-10-10T11:12:22.280Z"
  }
}
