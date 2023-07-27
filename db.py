from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connection_db = 'postgresql://postgres:123@localhost:5432/flask_db'

# Create a SQLAlchemy engine to connect to the PostgreSQL database.
# Replace 'postgres', '123', 'localhost', '5432', and 'flask_db' with your actual database credentials and name.
engine = create_engine(connection_db)

# Create a declarative base class for SQLAlchemy models.
# The 'Base' class will be the parent class for all the models defined in the application.
Base = declarative_base()

# Create a sessionmaker class to create session objects for interacting with the database.
# The 'bind=engine' argument associates the sessionmaker with the previously created engine,
# so all sessions created from this sessionmaker will use the same engine to communicate with the database.
Session = sessionmaker(bind=engine)
