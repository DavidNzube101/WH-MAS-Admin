from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin

import json
import os
import random

from .SarahDBClient.db import db
from .SarahDBClient.db import dbORM
from .SarahDBClient.encrypt import encrypter
import requests
from .DateToolKit import split_date
from . import id_generator
# from flask_debugtoolbar import DebugToolbarExtension
from . import function_pool
# from flask_profiler import Profiler

from . import ScreenGoRoute

if dbORM == None:
    User, Record = None, None


def initialize_app():
    app = Flask(__name__)
    # toolbar = DebugToolbarExtension(app)
    # profiler = Profiler(app)
    
    app.config['SECRET_KEY'] = 'FBETFBETFBET'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__).replace('\\', '/'), 'static/_UM_')
    print(f"UF: ({UPLOAD_FOLDER})")

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    from .admin_actions import admin_actions
    from .client_actions import client_actions
    from .client_actions2 import client_actions2
    from .payment_handler import payment_handler_actions

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin_actions, url_prefix='/')
    app.register_blueprint(payment_handler_actions, url_prefix='/')
    app.register_blueprint(client_actions, url_prefix='/')
    app.register_blueprint(client_actions2, url_prefix='/')

    @app.errorhandler(500)
    def internal_server_error(e, err_code=500):
        try:
            user = dbORM.get_all("UserIEEE")[f'{function_pool.isFound("UserIEEE", "id", current_user.id)}']
        except:
            user = "None"
        app.logger.error(f"Internal Server Error: {e}")
        return render_template('broken-page.html', err_id=id_generator.generateTID(), CUser=user, error=e, code=err_code), 500

    @app.errorhandler(404)
    def internal_server_error(e, err_code=404):
        try:
            user = dbORM.get_all("UserIEEE")[f'{function_pool.isFound("UserIEEE", "id", current_user.id)}']
        except:
            user = "None"
        app.logger.error(f"Route Not Found: {e}")
        return render_template('broken-page.html', err_id=id_generator.generateTID(), CUser=user, error=e, code=err_code), 404

    # @app.errorhandler(500)
    # def internal_server_error(e, err_code=500):
    #     app.logger.error(f"Internal Server Error: {e}")
    #     return render_template('broken-page.html', error=e, code=err_code), 500

    from flask_login import UserMixin, LoginManager

    FL_Login = LoginManager(app)
    FL_Login.login_view = 'login'

    class UserClass:
        def __init__(self, id):
            self.id = id

        @staticmethod
        def is_authenticated():
            return True

        @staticmethod
        def is_active():
            return True

        @staticmethod
        def is_anonymous():
            return False

        def get_id(self):
            return self.id


        @FL_Login.user_loader
        def load_user(id):
            try:
                u = function_pool.isFound("UserIEEE", "id", id)
                if not u:
                    return None
                return UserClass(id=dbORM.get_all("UserIEEE")[f'{u}']['id'])
            except:#Skipp
                anonymous = {
                    "0": {
                        "id": "0", 
                        "email": "NULL"
                    }
                }
                return UserClass(id=anonymous['0']['id'])


    @app.route("/login", methods=['GET', 'POST']) 
    def login():
        User = dbORM.get_all("UserIEEE")
        numbers = []
        for x in range(100):
            numbers.append(x)

        if request.method == 'POST':
            email = dbORM.sanitize_string(request.form.get('email'))
            password = dbORM.sanitize_string(request.form.get('password'))

            user = function_pool.isFound("UserIEEE", "email", email)


            if user and check_password_hash(dbORM.get_all("UserIEEE")[f'{user}']['password'], password):
                t_user = UserClass(id=f'{user}')
                login_user(t_user, remember=True)
                # flash("Join Tasklify Official WhatsApp Channel to get important updates and information.", category="Important_join")

                return redirect(url_for('views.dashboard'))
                
            else:
                user = function_pool.isFound("UserIEEE", "reg_number", email)
                

                if user and check_password_hash(dbORM.get_all("UserIEEE")[f'{user}']['password'], password):
                    t_user = UserClass(id=f'{user}')
                    login_user(t_user, remember=True)
                    # flash("Join Tasklify Official WhatsApp Channel to get important updates and information.", category="Important_join")

                    return redirect(url_for('views.dashboard'))
                else:
                    return render_template("login.html", status=("Incorrect password or email.", "Error occurred", {"email": email}), num_list=numbers)

        return render_template('login.html', status=("", "None", {"email": ""}), num_list=numbers)

    @app.route("/signup-refer/<string:username>")
    def referRegister(username):
        
        return render_template("onboarding.html", status=("", "None", "1"), ref_codee=username)

    @app.route("/signup", methods=['GET', 'POST'])
    def register():
        numbers = []
        for x in range(100):
            numbers.append(x)

        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')

            email = request.form.get('email')
            email_address = email

            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            # if function_pool.isFound("UserIEEE", "reg_number", request.form['reg_number'].replace(" ", "")):
            #     return render_template("onboarding.html", status=("Reg Number is already registered.", "Sign Up Error", "2"), num_list=numbers)


            user = function_pool.isFound("UserIEEE", 'email', email)#function_pool.isFound("UserIEEE", 'email', email)

            if user:
                return render_template("onboarding.html", status=("Email is already taken.", "Sign Up Error", "2", {"first_name": request.form['first_name'], "last_name": request.form['last_name'], "reg_number": request.form['reg_number'], "email": email_address}), num_list=numbers)
            elif len(email) < 4:
                return render_template("onboarding.html", status=("Email must be at least 4 characters long.", "Sign Up Error", "3", {"first_name": request.form['first_name'], "last_name": request.form['last_name'], "reg_number": request.form['reg_number'], "email": email_address}), num_list=numbers)
            elif len(request.form['reg_number']) < 5:
                return render_template("onboarding.html", status=("Reg Number must be more than 5 chracters.", "Sign Up Error", "3", {"first_name": request.form['first_name'], "last_name": request.form['last_name'], "reg_number": request.form['reg_number'], "email": email_address}), num_list=numbers)
            elif len(first_name) < 2 or len(last_name) < 2:
                return render_template("onboarding.html", status=("Name must be at least 2 characters long.", "Sign Up Error", "1", {"first_name": request.form['first_name'], "last_name": request.form['last_name'], "reg_number": request.form['reg_number'], "email": email_address}), num_list=numbers)
            elif password1 != password2:
                return render_template("onboarding.html", status=("Passwords do not match. Please re-enter your password.", "Sign Up Error", "1", {"first_name": request.form['first_name'], "last_name": request.form['last_name'], "reg_number": request.form['reg_number'], "email": email_address}), num_list=numbers)
            elif len(password1) < 8:
                return render_template("onboarding.html", status=("Password is too short. It must be at least 8 characters long.", "Sign Up Error", "1", {"first_name": request.form['first_name'], "last_name": request.form['last_name'], "reg_number": request.form['reg_number'], "email": email_address}), num_list=numbers)
            else:
                profile_pictures = ['mimi.png', 'aliyss.png', 'arrtective.png', 'english.jpg', 'narjiday.png', 'prof.jpg', 'bootlogo.png', 'community.jpg', 'hindi.jpg', 'grad1.jpg', 'grad2.jpg', 'grad3.jpg', 'grad4.jpg', 'grad5.jpg', 'grad6.jpg', 'grad7.jpg', 'grad8.jpg', 'grad9.jpg', 'grad10.jpg', 'grad11.jpg', 'grad12.jpg', 'grad13.jpg', 'grad14.jpg', 'grad15.jpg', 'grad16.jpg', 'grad17.jpg', 'grad18.jpg', 'grad19.jpg']
                new_user = {
                    'first_name': dbORM.sanitize_string(request.form['first_name'].replace(" ", "")) , 
                    'last_name': dbORM.sanitize_string(request.form['last_name'].replace(" ", "")), 
                    'password': generate_password_hash(password2), 
                    'email': request.form['email'].replace(" ", ""), 
                    'reg_number': dbORM.sanitize_string(request.form['reg_number'].replace(" ", "")), 
                    'department': request.form['department'], 
                    'faculty': request.form['faculty'], 
                    'institution': "", 
                    'onboarding_stage': "1", 
                    'level': request.form['level'],
                    "profile_picture": random.choice(profile_pictures),
                    "waitlist_apro_hire": "no",
                    "waitlist": "launched",
                    "tier": "basic",
                    "subscripton_datestamp": "None",
                    "subscripton_plan": "None"
                }

                dbORM.add_entry("UserIEEE", f"{encrypter(str(new_user))}")

                t_user = UserClass(id=f'{function_pool.isFound("UserIEEE", "email", email)}')

                login_user(t_user, remember=True)

                # flash("Join Official WhatsApp Channel", category="Important_join")

                return redirect(url_for('views.dashboard'))

        return render_template("onboarding.html", status=("", "None", "1", {"first_name": "", "last_name": "", "reg_number": "", "email": ""}), ref_codee="NULL", num_list=numbers)

    @app.route("/forgot-password")
    def forGotPasswordPage():
        
        return render_template("ForgotPassword.html")
        

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        # flash("Logged out successfully.", category='Success') 
        return redirect(url_for('views.welcome'))

    # import asyncio
    # from .SarahDBClient.SarahClient import cleanup

    # async def shutdown():
    #     await cleanup()

    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     asyncio.get_event_loop().run_until_complete(shutdown())
    

    return app