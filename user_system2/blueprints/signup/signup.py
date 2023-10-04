from flask import Blueprint, request, jsonify
from database import DatabaseHandler, db

signup_bp = Blueprint('signup_bp', __name__)

db.connect()
DatabaseHandler.create_table("user_data")


@signup_bp.route("/", methods=['POST'])
def signup():
    data = request.get_json()
    if not all(key in data for key in ("username", "password")):
        return jsonify({"message": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    if not username or not password:
        return {"message": "Username or password is blank. Please fill in both fields."}

    user_exist = DatabaseHandler.check_user_existence(username)
    password_exist = DatabaseHandler.check_password_existence(password)

    if user_exist and password_exist:
        return jsonify({"message": "user Already exist"}), 201
    else:
        create_user = DatabaseHandler.insert_record(username, password)
        if create_user:
            return jsonify({"message": f"User created successfully at id {create_user} "}), 201
        else:
            return jsonify({"message": "Failed to create user"}), 500



