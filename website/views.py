from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user


import base64
import imghdr
import datetime as dt
from datetime import datetime, timedelta

from . import DateToolKit as dtk
# from .db import db
# from .db import dbORM
# from . import encrypt
from . import function_pool
from . import ScreenGoRoute

from .SarahDBClient.db import db
from .SarahDBClient.db import dbORM
from .SarahDBClient import encrypt

# from . import app

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("UserAPRO"), None


today = dt.datetime.now().date()


views = Blueprint('views', __name__)

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else ''

def getDBItem(model, column, value):
    
    try:
        i = dbORM.get_all(model)[f'{function_pool.isFound(model, column, value)}']
    except Exception as e:
        i = {}

    return i



@views.route("/")
def welcome():
    # return redirect("https://dnextendedservices.pythonanywhere.com")
    return render_template("landing.html")

@views.route("/dashboard")
@login_required
def dashboard():
    # def calculateTimeDifference(dpt, ct):
    #     return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]
    
    # if dbORM.get_all("UserAPRO")[current_user.id]['waitlist'] != "launched":
    #     return render_template("WaitLobby.html", CUser=dbORM.get_all("UserAPRO")[current_user.id], TimeDifference=calculateTimeDifference, CurrentTime=function_pool.getDateTime()[1])
    # else:
    # return redirect("https://dnextendedservices.pythonanywhere.com/dashboard")
    return ScreenGoRoute.go_to("1", request=request)

@views.route("/waitlist")
@login_required
def waitlistScreen():
    def calculateTimeDifference(dpt, ct):
        return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]
    
    if dbORM.get_all("UserAPRO")[current_user.id]['waitlist'] != "launched":
        return render_template("WaitLobby.html", CUser=dbORM.get_all("UserAPRO")[current_user.id], TimeDifference=calculateTimeDifference, CurrentTime=function_pool.getDateTime()[1])
    else:
        return ScreenGoRoute.go_to("1", request=request)

@views.route('/submit-crash-report', methods=['POST'])
@login_required
def submitCrashReport():
    code = request.form['code']
    description = request.form['desc']
    error_id = request.form['error_id']
    user_reg_number = request.form['user_reg_number']
    _ = {
        'sender_id': "None",
        'recipient_id': "5",
        'title': f"Error Report",
        'content': f"A user has sent in a crash report.\nHere are the details:\n1. CODE: {code}\n2. DESCRIPTION: {description}\n3. ERROR ID: {error_id}\n",
        'type': "crash_report",
        "data": f"[2, 82]",
        'datestamp': f"{function_pool.getDateTime()[0]}",
        'timestamp': f"{function_pool.getDateTime()[1]}",
        'status': "delivered",
        "broadcast": "false"
    }

    dbORM.add_entry("NotificationAPRO", f"{encrypt.encrypter(str(_))}")

    return {"Message": "Success"}

@views.route("/dashboard/<string:screen_number>")
@login_required
def dashboardPages(screen_number):
    # def calculateTimeDifference(dpt, ct):
    #     return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]
    
    # if dbORM.get_all("UserAPRO")[current_user.id]['waitlist'] != "launched":
    #     return render_template("WaitLobby.html", CUser=dbORM.get_all("UserAPRO")[current_user.id], TimeDifference=calculateTimeDifference, CurrentTime=function_pool.getDateTime()[1])
    # else:
    return ScreenGoRoute.go_to(screen_number, request=request)

@views.route('/render-image', methods=['POST'])
@login_required
def renderImage():
    return render_template("ViewImage.html", assignment_id=request.form['assignment_id'], data_raw=request.form['base64_encoding'])