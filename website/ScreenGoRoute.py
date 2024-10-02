from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# from .db import dbORM
from . import DateToolKit as dtk

import base64
import imghdr
# from . import encrypt

# from .SarahDBClient.db import db
from .SarahDBClient.db import dbORM
# from .SarahDBClient.SarahClient import dbORM
from .SarahDBClient import encrypt

import random
from . import function_pool
import datetime as dt
from . import id_generator
from datetime import datetime

@login_required
def go_to(screen_id, _redirect=False, **kwargs):
	if _redirect:
		return redirect(url_for("views.dashboard"))

	u = dbORM.get_all("UserIEEE").get(str(current_user.id))
	print(">>>>>>>>>>>>>>>>>", current_user.id)
	if not u:
		flash("User not found", category=['EOC', 'Oops! Seems you will have to login again'])
		return redirect(url_for("login"))

	def tryGetKwargs(keyword, exception_text):
		try:
			return kwargs[keyword]
		except:
			return exception_text
	

	context = {
        'CUser': u,
        'ScreenID': screen_id,
        'DashboardTabs': ['All', 'Your Level', f'Today'],
        'ActiveDSH_Tab': tryGetKwargs('main_tab', 'All'),
        'DTK': dtk,
        'GetOppositeVisibility': function_pool.GetOppositeVisibility,
        'ToJoin': function_pool.toJoin,
        'DeviceType': function_pool.detectDeviceType(kwargs['request']),
        'WhichDevice': function_pool.which_device,
        'GetDBItem': function_pool.getDBItem,
        'DBORM': function_pool.dbORMJinja,
        'ShortenText': function_pool.shorten_text,
        'CurrentDate': function_pool.getDateTime()[0],
        'DecryptTYPE13': encrypt.decrypter,
        'ToInt': int,
        'LengthFunc': len,
        'ToStr': str,
        'ToFloat': float,
        'RandomID': id_generator.generateTID,
        'NoneType': None,
        'RoundFloat': round,
        'EnumerateFunc': enumerate,
		'ZipFunc': zip,
		'ToFloatToInt': function_pool.floatToInt,
        'PythonEval': function_pool.python_eval,
        'HideSensitive': function_pool.change_to_dots,
        'Thousandify': function_pool.thousandify,
        'getMIME': function_pool.get_mime_type,
        'TimeDifference': function_pool.calcTimeDifference,
        'CurrentTime': function_pool.getDateTime()[1],
        'HTMLBreak_': function_pool.HTMLBreak,
        'CONTRACT_CODE': function_pool.getContractCode(),
        'API_KEY': function_pool.getAPIKey(),
        'IsADPost': function_pool.IsADPost,
        'SECRET_KEY': function_pool.getSecretKey()
    }

    # Lazy loading of assignments
	# context['MyAssignments'] = function_pool.isFoundAll("AssignmentAPRO", "reg_number", u['reg_number'])
	# context['AllAssignments'] = dbORM.get_all("AssignmentAPRO").values()
	# context['AssignmentFilterTabs'] = ['All', 'Public', 'Private', 'Today', 'Done', 'Saved']
	# context['ActiveAFT_Tab'] = tryGetKwargs('active_tab', 'All')
	# context['AssignmentToView'] = tryGetKwargs('TheAssignmentToView', '')

	# Inserting ads :)
	# context['AllAssignments'] = function_pool.insertAds(interval=2, _list=context['AllAssignments'], ad_item={"visibility": "Public Ad", "reg_number": "1234567890"})

	# context['FilterAssignmentList'] = function_pool.insertAds(interval=2, _list=context['FilterAssignmentList'], ad_item={"visibility": "Public Ad", "reg_number": "1234567890"}) if tryGetKwargs('assignment_list', None) != None else context['FilterAssignmentList']
	# context['SearchResults'] = function_pool.insertAds(interval=1, _list=context['SearchResults'], ad_item={"visibility": "Public Ad", "reg_number": "1234567890"}) if tryGetKwargs('search_result', None) != None else context['SearchResults']

	# print()

	# Lazy loading of notifications
	notifications = dbORM.get_all("NotificationIEEE")
	context['UserNotifications'] = [n for n in notifications.values() if n['broadcast'] == "true" or n['recipient_id'] == u['id']]
	context['NotificationCount'] = sum(1 for n in context['UserNotifications'] if n['status'] == 'delivered' or n['broadcast'] == "true")
	context['NotificationCount'] = int(context['NotificationCount']) if int(context['NotificationCount'] )>= 10 else int(context['NotificationCount'])
	context['TheNotification'] = tryGetKwargs("the_notification", '')

	# Lazy loading of users
	users = dbORM.get_all("UserIEEE")
	context['UserList'] = [u for u in users.values() if u['tier'] != 'god' or u['reg_number'] != context['CUser']['reg_number']]

	# Components
	context['components'] = {
		"Note100Component": 'Note100-Component'
	}
	context['GetComponent'] = function_pool.getComponent # API for getting component data

	# Dynamic data
	for x, y in kwargs.items():
		context[f'{x}'] = y

	template = "admin-dashboard.html" if tryGetKwargs('admin_pass', None) else "dashboard.html"
	return render_template(template, **context)