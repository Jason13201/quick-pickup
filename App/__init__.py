from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "TeamCheesyFTW"

login_manager = LoginManager(app)

from App import routes
