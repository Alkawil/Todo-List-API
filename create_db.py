from flask import Flask
from app import db
from app import User
import os

def create_db():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/todo.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("instance/todo.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)
    with app.app_context():
        try:
            print("Creating tables...")
            db.create_all() 
            print("Database and tables created!")
        except Exception as e:
            print(f"Error creating database: {e}")

if __name__ == '__main__':
    create_db()

