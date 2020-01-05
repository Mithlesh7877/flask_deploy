from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
#what is environment variable find it?
app.config["SECRET_KEY"]='e832b0426cfad68ec55a8862a8e92dd1'
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"#these three slash give the relative path to the db 2 non create databse instance 
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='log'
login_manager.login_message_category='info'
from Napp import routes