from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Create an instance of the Flask class and assign it to the variable 'app'.
app = Flask(__name__)
#app.config["SECRET_KEY"] = "Matias"

# BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5434/flask_db_empty'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    date_joined = db.Column(db.DateTime)