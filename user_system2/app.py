from flask import Flask
from blueprints.signup.signup import signup_bp


app = Flask(__name__)
app.register_blueprint(signup_bp, url_prefix="/signup")

if __name__ == '__main__':
    app.run(debug=True)
