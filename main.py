from flask import Flask, jsonify, request, render_template
import pymysql 
import config
import os
from database import db
from models import DataEntry
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Use URL encoding for the '@' character in your password
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with this Flask app
db.init_app(app)


@app.route("/")
def index():
    # Renders the 'index.html' from the 'templates' folder
    return render_template("index.html")


### API Endpoint: Get All Data
@app.route("/api/data", methods=["GET"])
def get_all_data():
    data = DataEntry.query.all()
    results = [
        {
            "id": entry.id,
            "end_year": entry.end_year,
            "intensity": entry.intensity,
            "sector": entry.sector,
            "topic": entry.topic,
            "insight": entry.insight,
            "url": entry.url,
            "region": entry.region,
            "start_year": entry.start_year,
            "impact": entry.impact,
            "added": entry.added,
            "published": entry.published,
            "country": entry.country,
            "relevance": entry.relevance,
            "pestle": entry.pestle,
            "source": entry.source,
            "title": entry.title,
            "likelihood": entry.likelihood,
        }
        for entry in data
    ]
    return jsonify(results), 200


### API Endpoint: Filter Data by Sector, Region, Year
@app.route("/api/filter", methods=["GET"])
def filter_data():
    sector = request.args.get("sector")
    region = request.args.get("region")
    year = request.args.get("year")

    query = DataEntry.query

    if sector:
        query = query.filter(DataEntry.sector == sector)
    if region:
        query = query.filter(DataEntry.region == region)
    if year:
        query = query.filter((DataEntry.start_year == year) | (DataEntry.end_year == year))

    filtered_data = query.all()

    results = [
        {
            "id": entry.id,
            "end_year": entry.end_year,
            "intensity": entry.intensity,
            "sector": entry.sector,
            "topic": entry.topic,
            "insight": entry.insight,
            "url": entry.url,
            "region": entry.region,
            "start_year": entry.start_year,
            "impact": entry.impact,
            "added": entry.added,
            "published": entry.published,
            "country": entry.country,
            "relevance": entry.relevance,
            "pestle": entry.pestle,
            "source": entry.source,
            "title": entry.title,
            "likelihood": entry.likelihood,
        }
        for entry in filtered_data
    ]
    return jsonify(results), 200


@app.route("/api/distinct-values", methods=["GET"])
def get_distinct_values():
    # Distinct sectors
    distinct_sectors = db.session.query(DataEntry.sector).distinct().all()
    sectors = [s[0] for s in distinct_sectors if s[0]]

    # Distinct regions
    distinct_regions = db.session.query(DataEntry.region).distinct().all()
    regions = [r[0] for r in distinct_regions if r[0]]

    return jsonify({"sectors": sectors, "regions": regions}), 200


if __name__ == "__main__":
    app.run(debug=True)

