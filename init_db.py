from main import app
from database import db 
from models import DataEntry

with app.app_context():  
    db.create_all()  
    print(" Database tables created successfully!")
