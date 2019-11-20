from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from linebot import (
    LineBotApi, WebhookHandler
)
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DBADDRESS')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
line_bot_api = LineBotApi(os.getenv('LINE_API'))
handler = WebhookHandler(os.getenv('WEBHOOK'))

from un_line_bot import route
