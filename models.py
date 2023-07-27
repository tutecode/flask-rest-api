from sqlalchemy import Column, String, Integer
from db import Base, engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

# Define the Usuario class, representing the SQLAlchemy model for the 'usuario' table.
class Usuario(Base):
    # Set the table name to 'usuario'. In the database, this class will be mapped to a table named 'usuario'.
    __tablename__ = 'usuario'
    
    # Define the 'id' column as an Integer type, serving as the primary key for the table.
    # The 'autoincrement=True' attribute ensures that the 'id' value automatically increments for each new record.
    id = Column(Integer, autoincrement=True, primary_key=True)
    
    # Define the 'username' column as a String type with a maximum length of 70 characters.
    # The 'unique=True' attribute ensures that each username must be unique in the table.
    username = Column(String(70), unique=True)
    
    # Define the 'password' column as a String type with a maximum length of 70 characters.
    # It will store the password for each user.
    password = Column(String(200))

# Define the Ventas class, representing the SQLAlchemy model for the 'ventas' table.
class Ventas(Base):
    # Set the table name to 'ventas'. In the database, this class will be mapped to a table named 'ventas'.
    __tablename__ = 'ventas'
    
    # Define the 'id' column as an Integer type, serving as the primary key for the table.
    # The 'autoincrement=True' attribute ensures that the 'id' value automatically increments for each new record.
    id = Column(Integer, autoincrement=True, primary_key=True)
    
    # Define the 'username_id' column as an Integer, acting as a foreign key referencing the 'id' column of the 'usuario' table.
    username_id = Column(Integer, ForeignKey('usuario.id'))
    
    # Define the 'venta' column as an Integer.
    venta = Column(Integer)

# Create all the tables defined in the metadata of the 'Base' class within the specified 'engine'.
# This line ensures that the table corresponding to the "Usuario" model is created in the database.
Base.metadata.create_all(engine)
