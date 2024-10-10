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