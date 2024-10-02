from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user


import base64
import imghdr
import random
from datetime import datetime, timedelta
import datetime as dt

from . import DateToolKit as dtk
from .SarahDBClient.db import db
from .SarahDBClient.db import dbORM
from .SarahDBClient import encrypt
from . import ScreenGoRoute
from . import function_pool
from . import id_generator

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("UserAPRO"), None


today = dt.datetime.now().date()


admin_actions = Blueprint('admin_actions', __name__)
aa = admin_actions

