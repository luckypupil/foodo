#!/usr/bin/env python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.admin import Admin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models, forms, helper