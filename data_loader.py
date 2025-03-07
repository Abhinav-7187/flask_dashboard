import json
from main import app
from database import db
from models import DataEntry

# Load JSON data from the file
with open("jsondata.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Parse JSON file

# Function to convert empty strings to None (NULL in MySQL)
def clean_value(value, is_int=False):
    if value == "" or value is None:
        return None
    return int(value) if is_int else value  # Convert to int if required

# Insert data into MySQL
with app.app_context():
    for entry in data:
        new_entry = DataEntry(
            end_year=clean_value(entry.get("end_year")),
            intensity=clean_value(entry.get("intensity"), is_int=True),
            sector=clean_value(entry.get("sector")),
            topic=clean_value(entry.get("topic")),
            insight=clean_value(entry.get("insight")),
            url=clean_value(entry.get("url")),
            region=clean_value(entry.get("region")),
            start_year=clean_value(entry.get("start_year")),
            impact=clean_value(entry.get("impact")),
            added=clean_value(entry.get("added")),
            published=clean_value(entry.get("published")),
            country=clean_value(entry.get("country")),
            relevance=clean_value(entry.get("relevance"), is_int=True),
            pestle=clean_value(entry.get("pestle")),
            source=clean_value(entry.get("source")),
            title=clean_value(entry.get("title")),
            likelihood=clean_value(entry.get("likelihood"), is_int=True)
        )
        db.session.add(new_entry)  # Add to session

    db.session.commit()  # Commit all changes
    print(" JSON Data Successfully Inserted into MySQL!")
