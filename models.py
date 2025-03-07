from database import db

# Define a model based on JSON structure
class DataEntry(db.Model):
    __tablename__ = "data_entry"  # Make sure matches your actual table name
    
    id = db.Column(db.Integer, primary_key=True)
    end_year = db.Column(db.String(10))
    intensity = db.Column(db.Integer)
    sector = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    insight = db.Column(db.Text)
    url = db.Column(db.String(500))
    region = db.Column(db.String(255))
    start_year = db.Column(db.String(10))
    impact = db.Column(db.String(10))
    added = db.Column(db.String(50))
    published = db.Column(db.String(50))
    country = db.Column(db.String(255))
    relevance = db.Column(db.Integer)
    pestle = db.Column(db.String(255))
    source = db.Column(db.String(255))
    title = db.Column(db.Text)
    likelihood = db.Column(db.Integer)

    def __repr__(self):
        return f"<DataEntry {self.title}>"

