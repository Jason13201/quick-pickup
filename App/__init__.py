from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "TeamCheesyFTW"

login_manager = LoginManager(app)
socketio = SocketIO(app, logger=True, engineio_logger=True)

from App import routes
