from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user


import base64
import random
import requests
import imghdr
import json
import datetime as dt

from . import DateToolKit as dtk
# from .db import db
from . import id_generator
# from .db import dbORM
from . import function_pool
# from . import encrypt
from . import ScreenGoRoute

from .SarahDBClient.db import db
from .SarahDBClient.db import dbORM
from .SarahDBClient import encrypt

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("UserAPRO"), None


today = dt.datetime.now().date()


payment_handler_actions = Blueprint('payment_handler_actions', __name__)
pha = payment_handler_actions

is_test = True


# ------------------------------------------------------------------------------------------------------------------
@pha.route("/proceed-payments", methods=['POST'])
@login_required
def proceedPayments():

    auth_headers ={
        "Authorization": "Bearer sk_test_f78985abaed4ccc2a202762c3a111ef08b6b5b8f",
        "Content-Type": "application/json"
    }
    customer_email = dbORM.get_all('UserAPRO')[f'{current_user.id}']['email']
    auth_data = { "email": customer_email, "amount": f"{request.form['amount']}00" } #"{}".format(products[product_id]['price'])
    auth_data = json.dumps(auth_data)
    req = requests.post('https://api.paystack.co/transaction/initialize', headers=auth_headers, data=auth_data)
    response_data = json.loads(req.text)
    try:
        paystack_uri = response_data['data']['authorization_url']
        return redirect(paystack_uri)
    except Exception as e:
        flash("Paystack is experiencing some issues. Please wait and try again later", category=['EOC', "Payment service down"])
        return ScreenGoRoute.go_to("6", request=request)

@pha.route("/update-user-details", methods=['POST'])
def UpdateUser():
    amount = request.form['amount']
    user_id = request.form['user_id']
    status = request.form['status']
    u = dbORM.get_all("UserAPRO")[f'{function_pool.isFound("UserAPRO", "id", user_id)}']
    
    
    if status == "SUCCESS":
        if "250" in amount:
            dbORM.update_entry(
            "UserAPRO", 
            f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
            encrypt.encrypter(str({
                "tier": "pro",
                "subscripton_plan": "month",
                "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
                "subscription_datestamp_next": f"{function_pool.getNextBillingDate('month')}"
                })),
            False
            )
        elif "800" in amount:
            dbORM.update_entry(
            "UserAPRO", 
            f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
            encrypt.encrypter(str({
                "tier": "pro",
                "subscripton_plan": "semester",
                "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
                "subscription_datestamp_next": f"{function_pool.getNextBillingDate('semester')}"
                })),
            False
            )
        elif "400" in amount:
            dbORM.update_entry(
            "UserAPRO", 
            f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
            encrypt.encrypter(str({
                "tier": "advanced",
                "subscripton_plan": "month",
                "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
                "subscription_datestamp_next": f"{function_pool.getNextBillingDate('month')}"
                })),
            False
            )
        elif "1200" in amount:
            dbORM.update_entry(
            "UserAPRO", 
            f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
            encrypt.encrypter(str({
                "tier": "advanced",
                "subscripton_plan": "semester",
                "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
                "subscription_datestamp_next": f"{function_pool.getNextBillingDate('semester')}"
                })),
            False
            )

        return "Success"
    elif status == "USER_CANCELLED":
        return "cancelled"

    else:
        return "failed"
    
    

@pha.route("/callback")
@login_required
def showSuccess():
    ref = request.args['trxref']
    auth_headers ={
        "Authorization": "Bearer sk_test_f78985abaed4ccc2a202762c3a111ef08b6b5b8f",
        "Content-Type": "application/json"
    }
    req = requests.get('https://api.paystack.co/transaction/verify/{}'.format(ref), headers=auth_headers)
    tr_data = json.loads(req.text)
    message = tr_data['data']['status']
    amount = tr_data['data']['amount']
    amount = (amount/100)
    amount = "{:.2f}".format(amount)
    tr_id = tr_data['data']['id']
    if "250" in amount:
        dbORM.update_entry(
        "UserAPRO", 
        f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
        encrypt.encrypter(str({
            "tier": "pro",
            "subscripton_plan": "month",
            "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
            "subscription_datestamp_next": f"{function_pool.getNextBillingDate('month')}"
            })),
        False
        )
    elif "850" in amount:
        dbORM.update_entry(
        "UserAPRO", 
        f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
        encrypt.encrypter(str({
            "tier": "pro",
            "subscripton_plan": "semester",
            "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
            "subscription_datestamp_next": f"{function_pool.getNextBillingDate('semester')}"
            })),
        False
        )
    elif "400" in amount:
        dbORM.update_entry(
        "UserAPRO", 
        f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
        encrypt.encrypter(str({
            "tier": "advanced",
            "subscripton_plan": "month",
            "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
            "subscription_datestamp_next": f"{function_pool.getNextBillingDate('month')}"
            })),
        False
        )
    elif "1200" in amount:
        dbORM.update_entry(
        "UserAPRO", 
        f"{function_pool.isFound('UserAPRO', 'id', str(current_user.id))}", 
        encrypt.encrypter(str({
            "tier": "advanced",
            "subscripton_plan": "semester",
            "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
            "subscription_datestamp_next": f"{function_pool.getNextBillingDate('semester')}"
            })),
        False
        )
    
    return render_template('CheckoutSuccess.html', CUser=dbORM.get_all("UserAPRO")[f'{current_user.id}'], tr_id=tr_id, message=message, price=amount, DTK = dtk)