import datetime
import json
from functools import wraps

import jwt
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from db import Session, engine, connection_db
from models import Usuario
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy


# Create an instance of the Flask class and assign it to the variable 'app'.
app = Flask(__name__)
app.config["SECRET_KEY"] = "Matias"

# BD
app.config['SQLALCHEMY_DATABASE_URI'] = connection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

session = Session()


# This is a route decorator that defines a route for the '/hola' URL path.
# It specifies that the route will handle HTTP GET requests.
@app.route("/hola", methods=["GET"])
def hola():
    # The function associated with this route, 'hola()', will be executed when the endpoint is accessed.
    # It returns a JSON response containing a message.
    return jsonify({"message": "Endpoint desde hola"})


@app.route("/create_user", methods=["POST"])
def create_user():
    # This route handles a POST request to the "/create_user" endpoint.

    # Load the JSON data from the request's body.
    data = json.loads(request.data)

    # Check if "username" and "password" keys are present in the JSON data.
    if "username" not in data:
        return jsonify({"respuesta": "No estas enviando el username!"})
    if "password" not in data:
        return jsonify({"respuesta": "No estas enviando el password!"})

    # Check if the "username" and "password" values are not empty.
    if len(data["username"]) == 0:
        return jsonify({"respuesta": "Username no puede estar vacío."})
    if len(data["password"]) == 0:
        return jsonify({"respuesta": "Password no puede estar vacío."})

    # Establish a connection to the database using the SQLAlchemy engine.
    with engine.connect() as con:
        # Convert password to sha256
        hash_password = generate_password_hash(data["password"], method="sha256")
        # Create a new instance of the Usuario model with the provided username and password.
        nuevo_usuario = Usuario(username=data["username"], password=hash_password)

        # Add the newly created user to the current session.
        session.add(nuevo_usuario)

        try:
            # Commit the changes to the database.
            session.commit()

        except Exception as e:
            print("Error:", str(e))
            return jsonify({"respuesta": "Usuario ya esta creado en la base de datos!"})

    # If the user creation is successful, return a JSON response.
    return jsonify({"respuesta": "Usuario creado correctamente!"})


# This is a decorator function 'token_required' that adds authentication and authorization
# to the protected routes. It checks for a valid JSON Web Token (JWT) in the request headers
# under the key "x-access-tokens".
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
       
        # Check if the "x-access-tokens" key is present in the request headers.
        if "x-access-tokens" in request.headers:
            # If present, retrieve the token value from the headers.
            token = request.headers["x-access-tokens"]

        # If no token is provided, return an error response.
        if not token:
            return jsonify({"message": "a valid token is missing"})

        try:
            # Decode the JWT using the application's SECRET_KEY to retrieve the token payload.
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            # If decoding fails (e.g., invalid token), return an error response.
            return jsonify({"message": "token is invalid"})
        # If the token is valid, continue to the route function (endpoint).
        return f(*args, **kwargs)

    # Return the decorator function itself.
    return decorator


@app.route("/login", methods=["GET"])
def login_user():
    # Retrieve the HTTP Basic Authentication credentials from the request.
    auth = request.authorization

    # Check if the username and password are provided in the authentication credentials.
    if not auth or not auth.username or not auth.password:
        return jsonify({"Response": "Could not verify"})

    # Establish a connection to the database using the SQLAlchemy engine.
    with engine.connect() as con:
        # Form a SQL query to retrieve the user's information based on the provided username.
        query = f"SELECT * FROM usuario WHERE username = '{auth.username}';"

        # Execute the query and fetch the first result (user information) using 'fetchone()'.
        user = con.execute(text(query)).fetchone()

    # Print the fetched user information (debugging purposes).
    print(user)

    if user is not None:
        # The user is found, so we can access the 'password' attribute at index 2 (0-based index).
        # Check if the provided password matches the hashed password stored in the database.
        if check_password_hash(user[2], auth.password):
            # If the password is correct, create a new JWT for the user with a public_id claim,
            # and set its expiration time to 30 minutes from the current time.
            token = jwt.encode(
                {
                    "public_id": user[1],  # Use 'public_id' from the fetched user info
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                app.config[
                    "SECRET_KEY"
                ],  # Use the application's secret key for encoding
                algorithm="HS256",  # Specify the algorithm for token encoding
            )
            # Return the generated token in a JSON response.
            return jsonify({"token": token})
        else:
            # If the password is incorrect, return an error response.
            return jsonify({"Response": "Password incorrect"})

    # If the user is not found, return an error response indicating login is required.
    return jsonify({"Response": "Login requerido"})


@app.route("/obtener_venta", methods=["GET"])
# Validate first if the user has a token
@token_required
def obtener_venta():
    # Load the JSON data from the request's body.
    data = json.loads(request.data)
    print(data)  # Debugging: Print the received data to the console.

    # Check if 'username' key is present in the JSON data.
    if "username" not in data:
        return jsonify({"respuesta": "Username no enviado, validar datos!"})

    # Establish a connection to the database using the SQLAlchemy engine.
    with engine.connect() as con:
        # Form a SQL query to retrieve the user's information based on the provided username.
        obtener_usuario = (
            f"SELECT * FROM usuario WHERE username = '{data['username']}';"
        )
        respuesta = con.execute(text(obtener_usuario)).fetchone()
        print(respuesta)
        print(respuesta)

        # Form a SQL query to retrieve sales data for the user.
        obtener_venta = (
            f"SELECT venta FROM ventas WHERE username_id = '{respuesta[0]}';"
        )
        respuesta_ventas = con.execute(text(obtener_venta))

        # Extract the sales data from the query results.
        # The result of con.execute(obtener_venta) is a list of tuples, and we extract the first element from each tuple to get the 'venta' value.
        respuesta_ventas = [i[0] for i in respuesta_ventas]

        # Return a JSON response containing the sales data for the user.
        return jsonify(
            {
                "ventas_usuario": {
                    "usuario": data["username"],
                    "ventas": respuesta_ventas,
                }
            }
        )


# The following block is a conditional check. When the script is run directly (not imported as a module),
# the '__name__' variable is set to '__main__'. This block ensures that the app only runs when executed as the main module.
if __name__ == "__main__":
    # Start the Flask development server.
    # The 'debug=True' argument enables debug mode, which provides additional error information
    # and auto-reloads the server whenever you make changes to the code, making development easier.
    app.run(debug=True)
