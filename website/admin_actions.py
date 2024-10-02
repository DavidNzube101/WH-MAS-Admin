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

@aa.route("/admin-dashboard")
def enterAdminDBOARD():

    if function_pool.isAdmin(current_user.id) == True:
        return ScreenGoRoute.go_to("1", request=request, admin_pass=id_generator.generateTID())
    else:
        flash("You are restricted from accessing this.", category=['EOC', 'Access denied'])
        return ScreenGoRoute.go_to("1", request=request)

@aa.route("/admin-dashboard/<string:screen_id>")
def enterAdminDBOARDSceen(screen_id):

    if function_pool.isAdmin(current_user.id) == True:
        return ScreenGoRoute.go_to(screen_id, request=request, admin_pass=id_generator.generateTID())
    else:
        flash("You are restricted from accessing this.", category=['EOC', 'Access denied'])
        return ScreenGoRoute.go_to("1", request=request)

@aa.route("/add-broadcast", methods=['POST'])
def AddBroadCast():
    if function_pool.isAdmin(current_user.id) == True:

        _ = {
            "sender_id": "None", 
            "recipient_id": "None", 
            "title": request.form['title'].replace("'", "").replace('"', ""), 
            "content": request.form['content'].replace("'", "").replace('"', ""), 
            "type": "official", 
            "data": request.form['data'], 
            "datestamp": f"{function_pool.getDateTime()[0]}", 
            "timestamp": f"{function_pool.getDateTime()[1]}", 
            "status": "delivered", 
            "broadcast": "true"
        }
        dbORM.add_entry("NotificationAPRO", f"{encrypt.encrypter(str(_))}")
        flash(f"Successfully broadcasted message '{request.form['title']}'.", category=['SUC', 'Message Broadcasted'])

        return ScreenGoRoute.go_to("9", request=request, admin_pass=id_generator.generateTID())
    else:
        flash("You are restricted from accessing this.", category=['EOC', 'Access denied'])
        return ScreenGoRoute.go_to("9", request=request)

@aa.route('/open-broadcast/<string:notification_id>')
def showBroadcast(notification_id):
    try:
        the_notification = dbORM.get_all("NotificationAPRO")[f'{function_pool.isFound("NotificationAPRO", "id", notification_id)}']
        dbORM.update_entry(
            "NotificationAPRO", 
            f"{function_pool.isFound('NotificationAPRO', 'id', notification_id)}", 
            encrypt.encrypter(str(
                {
                    "status": "read"
                }
            )), 
            dnd=False
        )
        return ScreenGoRoute.go_to("8", request=request, the_notification=the_notification)
    except Exception as e:
        flash(f"Error occured while retriving message. Try again later.{e} ", category=['EOC', 'Message load unsuccessful'])

        return ScreenGoRoute.go_to("8", request=request)

@aa.route("/delete-broadcast/<string:notification_id>")
def deleteBroadcast(notification_id):
    if function_pool.isAdmin(current_user.id) == True:
        dbORM.delete_entry("NotificationAPRO", function_pool.isFound("NotificationAPRO", "id", notification_id))

        flash(f"Deleted Broadcast!", category=['SUC', 'Deleted successfully'])

        return ScreenGoRoute.go_to("9", request=request, admin_pass=id_generator.generateTID())
    else:
        flash("You are restricted from accessing this.", category=['EOC', 'Access denied'])
        return ScreenGoRoute.go_to("1", request=request)

@aa.route("/delete-user/<string:user_id>")
def deleteUser(user_id):
    if function_pool.isAdmin(current_user.id) == True:
        try:
            dbORM.delete_entry("UserAPRO", function_pool.isFound("UserAPRO", "id", user_id))

            flash(f"Deleted User!", category=['SUC', 'Deleted successfully'])

            return ScreenGoRoute.go_to("10", request=request, admin_pass=id_generator.generateTID())
        except:
            return ScreenGoRoute.go_to("10", request=request, admin_pass=id_generator.generateTID())

    else:
        flash("You are restricted from accessing this.", category=['EOC', 'Access denied'])
        return ScreenGoRoute.go_to("1", request=request)


@aa.route("/exit-user-from-lobby/<string:user_id>")
def leaveLobby(user_id):

    if function_pool.isAdmin(current_user.id) == True:
        try:
            dbORM.update_entry(
                "UserAPRO", 
                f"{function_pool.isFound('UserAPRO', 'id', user_id)}", 
                encrypt.encrypter(str(
                    {
                        "waitlist": "launched"
                    }
                )), 
                dnd=False
            )
            flash(f"Deleted User!", category=['SUC', 'Deleted successfully'])
        except:
            pass

        return ScreenGoRoute.go_to("10", request=request, admin_pass=id_generator.generateTID())


    else:
        flash("You are restricted from accessing this.", category=['EOC', 'Access denied'])
        return ScreenGoRoute.go_to("1", request=request)

@aa.route("/create-note", methods=['GET', 'POST'])
def create_note():

    if request.method == 'GET':
        return ScreenGoRoute.go_to("19", request=request)
    else:
        N100_CONTENT = f"{request.form['N100-content']}".replace("'", "").replace('"', '')
        if function_pool.isFound('Notes', 'name', request.form['N100-name']) == None:
            
            _ = {
                "name": request.form['N100-name'],
                "content": f"{request.form['N100-content']}".replace("'", "").replace('"', ''),
                "timestamp": function_pool.getDateTime()[1],
                "datestamp": function_pool.getDateTime()[0],
                'lecturer': request.form['N100-lecturer'],
                'is_premium': request.form['N100-is_premium'],
                'textbook': request.form['N100-textbook'],
                'manual': request.form['N100-manual']
            }

            dbORM.add_entry("Notes", f'{encrypt.encrypter(str(_))}')
        else:
            flash(f'Already added note {request.form["N100-name"]}', category=['WWE', 'Added already!'])

        return ScreenGoRoute.go_to("19", request=request)















# if function_pool.isAdmin(current_user.id) == True:
#     return ScreenGoRoute.go_to("1", request=request, admin_pass=id_generator.generateTID())
# else:
#     flash("You are restricted from accessing this.", category=['EOC', 'Access denied'])
#     return ScreenGoRoute.go_to("1", request=request)