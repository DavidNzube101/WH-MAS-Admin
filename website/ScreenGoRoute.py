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
from . import study_materials
import datetime as dt
from . import id_generator
from datetime import datetime

# User, Record = dbORM.get_all("UserAPRO"), None
	
								# <!-- <img src="data:{{ getMIME( Task['image_raw'] ) }};base64,{{ Task['image_raw'] }}" style="background: white; aspect-ratio: 1/1; width: 40px; padding: 20px; object-fit: cover;"> -->


# def go_to(screen_id, _redirect=False, **kwargs):
# 	if _redirect == False:
# 		u = dbORM.get_all("UserAPRO")[f'{current_user.id}']

# 		def checkImagePassError(image_raw):
# 			try:
# 				rr = f"data:{function_pool.getMIME(image_raw)};base64,{image_raw}"
# 				return "false"
# 			except:
# 				return "true"


# 		all_assignments = []
# 		Assignment = dbORM.get_all("AssignmentAPRO")
# 		for x, y in Assignment.items():
# 			all_assignments.append(y)

# 		my_assignments = function_pool.isFoundAll("AssignmentAPRO", "reg_number", u['reg_number'])

# 		# flash("Hey this is a flash", category=["SUC", "Changed Profile Picture"])

# 		def tryGetKwargs(keyword, exception_text):

# 			try:
# 				return kwargs[keyword]
# 			except:
# 				return exception_text

# 		my_assignments = tryGetKwargs('the_assignment', function_pool.isFoundAll("AssignmentAPRO", "reg_number", u['reg_number']))
# 		active_tab = tryGetKwargs('active_tab', 'All')
# 		assignment_to_view = tryGetKwargs('TheAssignmentToView', '')
# 		main_tab = tryGetKwargs('main_tab', 'All')
# 		assignment_list = tryGetKwargs('assignment_list', None)
# 		search_result = tryGetKwargs('search_result', None)
# 		search_input = tryGetKwargs('search_input', '')
# 		the_notification = tryGetKwargs("the_notification", '')

# 		assignments = dbORM.get_all("AssignmentAPRO")
# 		normal_assignment_list = []
# 		for x, y in assignments.items():
# 			if y['reg_number'] != u['reg_number']:
# 				normal_assignment_list.append(y)

# 		# print(len(assignment_list), len(search_result))

# 		normal_assignment_list = None if normal_assignment_list == [] else normal_assignment_list[::-1]

# 		if assignment_list == None and search_result == None:
# 			normal_assignment_list = normal_assignment_list
# 		elif assignment_list == None or search_result == None:	
# 			if assignment_list == None:	
# 				normal_assignment_list = None
# 			elif search_result == None:	
# 				normal_assignment_list = None
# 		else:
# 			normal_assignment_list = None if (len(assignment_list) > 0 or len(search_result) > 0) else normal_assignment_list

# 		print(">>>>>>>>>>>>>>>>>>>>>>", (assignment_list), (search_result))

# 		try:
# 			assignment_list = assignment_list[::-1]
# 		except:
# 			pass

# 		try:
# 			search_result = search_result[::-1]
# 		except:
# 			pass

# 		try:
# 			Notifications = dbORM.get_all("NotificationAPRO")
# 			my_notifications = []
# 			new_notifications = []
# 			for x, y in Notifications.items():
# 				if y['broadcast'] == "true":
# 					my_notifications.append(y)

# 				elif y['recipient_id'] == u['id']:
# 					my_notifications.append(y)

# 				if ((y['recipient_id'] == u['id']) and (y['status'] == 'delivered')) or y['broadcast'] == "true" :
# 					new_notifications.append(y)
# 		except KeyError as e:
# 			my_notifications = function_pool.isFoundAll("NotificationAPRO", "recipient_id", u['id'])
# 			new_notifications = function_pool.isFoundAll("NotificationAPRO", "status", "delivered")

# 		users = dbORM.get_all("UserAPRO")
# 		user_list = []
# 		for x, y in users.items():
# 			if y['tier'] != 'god':
# 				user_list.append(y)

# 			elif y['reg_number'] != u['reg_number']:
# 				user_list.append(y)

# 		voho_study_materials = study_materials.Materials()

# 		user_forms = []
# 		for x, y in dbORM.get_all("FormAPRO").items():
# 			if x != "0" and y['reg_number'] == u['reg_number']:
# 				user_forms.append(y)

# 		if u['waitlist'] == "not_decided":
# 			dbORM.update_entry(
#                 "UserAPRO", 
#                 f"{function_pool.isFound('UserAPRO', 'id', u['id'])}", 
#                 encrypt.encrypter(str(
#                     {
#                         "tier": "pro",
#                         "subscripton_plan": "month",
#                         "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
#                         "subscription_datestamp_next": f"{function_pool.getNextBillingDate('month')}",
#                         "waitlist": "launched"
#                     }
#                 )), 
#                 dnd=False
#             )
# 			flash(f"Hey {u['first_name']}, you've been gifted a Voho Pro subscription for one month.", category=['SUC', 'Voho Pro'])
# 			redirect(url_for("views.dashboard"))

# 		return render_template("dashboard.html" if tryGetKwargs('admin_pass', None) == None else "admin-dashboard.html",
# 			CUser = u,		
# 			UserList = user_list,
# 			ImagePassError = checkImagePassError,
# 			UserForms = user_forms[::-1],
# 			FormID = tryGetKwargs("form_id", "None"),
# 			StudyMaterials = voho_study_materials.all_materials(),
# 			AllAssignments = all_assignments[::-1],
# 			MyAssignments = my_assignments[::-1],
# 			AssignmentFilterTabs = ['All', 'Public', 'Private', 'Today', 'Done', 'Saved'], #AFT
# 			ActiveAFT_Tab = active_tab,
# 			AssignmentToView = assignment_to_view,
# 			ScreenID = screen_id,
# 			DashboardTabs = ['All', 'Your Level', f'Today - {u["level"]}L'],
# 			ActiveDSH_Tab = main_tab,
# 			FilterAssignmentList = assignment_list,# if (len(normal_assignment_list) == 0 and len(search_result) == 0) else None,
# 			SearchResults = search_result,# if (len(assignment_list) == 0 and len(normal_assignment_list) == 0) else None,
# 			SearchInput = search_input,
# 			NormalAssignmentList = normal_assignment_list,
# 			UserNotifications = my_notifications[::-1],
# 			NotificationCount = len(new_notifications) if len(new_notifications) < 10 else "9+",
# 			TheNotification = the_notification,
# 			DTK = dtk,
# 			ApprovedSubjectList = function_pool.return_approved_subjects(),
# 			LengthFunc = len,
# 			GetOppositeVisibility = function_pool.GetOppositeVisibility,
# 			ToJoin = function_pool.toJoin,
# 			RandomSearchText = function_pool.RandomSearchText,
# 			DeviceType = function_pool.detectDeviceType(kwargs['request']),
# 			WhichDevice = function_pool.which_device,
# 			NoneType = None,
# 			GetDBItem = function_pool.getDBItem,
# 			ToString = str,
#         	DBORM = function_pool.dbORMJinja,
# 			ShortenText = function_pool.shorten_text,
# 			RoundFloat = round,
# 			CurrentDate = function_pool.getDateTime()[0],
# 			ToFloat = float,
# 			ToInt = int,
# 			RemoveAdmins = function_pool.removeAdmins,
# 			ReturnFaculty = function_pool.return_faculty,
# 			CurrencyExchange = function_pool.CurrencyExchange(),
# 			DecryptTYPE13 = encrypt.decrypter,
# 			RandomID = id_generator.generateTID,
# 			PythonEval = function_pool.python_eval,
# 			HideSensitive = function_pool.change_to_dots,
# 			EnumerateFunc = enumerate,
# 			ZipFunc = zip,
# 			ToFloatToInt = function_pool.floatToInt,
# 			Thousandify = function_pool.thousandify,
# 			getMIME = function_pool.get_mime_type,
# 			TimeDifference = function_pool.calcTimeDifference,
# 			CurrentTime = function_pool.getDateTime()[1],
# 			HTMLBreak_ = function_pool.HTMLBreak,
# 			CONTRACT_CODE = function_pool.getContractCode(),
# 			API_KEY = function_pool.getAPIKey(),
# 			SECRET_KEY = function_pool.getSecretKey()
# 		)
# 	else:
# 		return redirect(url_for("views.dashboard"))
	







# from flask import render_template, redirect, url_for, flash
# from flask_login import login_required, current_user
# from .SarahDBClient.db import dbORM
# from . import DateToolKit as dtk
# from . import function_pool
# from . import study_materials
# import datetime as dt

@login_required
def go_to(screen_id, _redirect=False, **kwargs):
	if _redirect:
		return redirect(url_for("views.dashboard"))

	u = dbORM.get_all("UserAPRO").get(str(current_user.id))
	print(">>>>>>>>>>>>>>>>>", current_user.id)
	if not u:
		flash("User not found", category=['EOC', 'Oops! Seems you will have to login again'])
		return redirect(url_for("login"))

	def tryGetKwargs(keyword, exception_text):
		try:
			return kwargs[keyword]
		except:
			return exception_text
	
	normal_assignment_list = []
	for x, y in dbORM.get_all("AssignmentAPRO").items():
		if y['reg_number'] != u['reg_number']:
			normal_assignment_list.append(y)

	normal_assignment_list = None if normal_assignment_list == [] else normal_assignment_list[::-1]

	if tryGetKwargs('assignment_list', None) == None and tryGetKwargs('search_result', None) == None:
		normal_assignment_list = normal_assignment_list
	elif tryGetKwargs('assignment_list', None) == None or tryGetKwargs('search_result', None) == None:	
		if tryGetKwargs('assignment_list', None) == None:	
			normal_assignment_list = None
		elif tryGetKwargs('search_result', None) == None:	
			normal_assignment_list = None
	else:
		normal_assignment_list = None if (len(tryGetKwargs('assignment_list', None)) > 0 or len(tryGetKwargs('search_result', None)) > 0) else normal_assignment_list

	context = {
        'CUser': u,
        'ScreenID': screen_id,
        'DashboardTabs': ['All', 'Your Level', f'Today - {u["level"]}L'],
        'ActiveDSH_Tab': tryGetKwargs('main_tab', 'All'),
        'DTK': dtk,
        'FilterAssignmentList': tryGetKwargs('assignment_list', None),
        'MyAssignments': tryGetKwargs('the_assignment', function_pool.isFoundAll("AssignmentAPRO", "reg_number", u['reg_number']))[::-1],
        'SearchResults': tryGetKwargs('search_result', None),
        'SearchInput': tryGetKwargs('search_input', ''),
        'ApprovedSubjectList': function_pool.return_approved_subjects(),
        'GetOppositeVisibility': function_pool.GetOppositeVisibility,
        'ToJoin': function_pool.toJoin,
        'RandomSearchText': function_pool.RandomSearchText,
        'DeviceType': function_pool.detectDeviceType(kwargs['request']),
        'WhichDevice': function_pool.which_device,
        'GetDBItem': function_pool.getDBItem,
        'NormalAssignmentList': normal_assignment_list[::-1] if normal_assignment_list != None else normal_assignment_list,
        'DBORM': function_pool.dbORMJinja,
        'ShortenText': function_pool.shorten_text,
        "ReturnFaculty": function_pool.return_faculty,
        'CurrentDate': function_pool.getDateTime()[0],
        'CurrencyExchange': function_pool.CurrencyExchange(),
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

	print(context['NormalAssignmentList'])

    # Lazy loading of assignments
	context['MyAssignments'] = function_pool.isFoundAll("AssignmentAPRO", "reg_number", u['reg_number'])
	context['AllAssignments'] = dbORM.get_all("AssignmentAPRO").values()
	context['AssignmentFilterTabs'] = ['All', 'Public', 'Private', 'Today', 'Done', 'Saved']
	context['ActiveAFT_Tab'] = tryGetKwargs('active_tab', 'All')
	context['AssignmentToView'] = tryGetKwargs('TheAssignmentToView', '')

	# Inserting ads :)
	# context['AllAssignments'] = function_pool.insertAds(interval=2, _list=context['AllAssignments'], ad_item={"visibility": "Public Ad", "reg_number": "1234567890"})

	# context['FilterAssignmentList'] = function_pool.insertAds(interval=2, _list=context['FilterAssignmentList'], ad_item={"visibility": "Public Ad", "reg_number": "1234567890"}) if tryGetKwargs('assignment_list', None) != None else context['FilterAssignmentList']
	# context['SearchResults'] = function_pool.insertAds(interval=1, _list=context['SearchResults'], ad_item={"visibility": "Public Ad", "reg_number": "1234567890"}) if tryGetKwargs('search_result', None) != None else context['SearchResults']

	# print()

	# Lazy loading of notifications
	notifications = dbORM.get_all("NotificationAPRO")
	context['UserNotifications'] = [n for n in notifications.values() if n['broadcast'] == "true" or n['recipient_id'] == u['id']]
	context['NotificationCount'] = sum(1 for n in context['UserNotifications'] if n['status'] == 'delivered' or n['broadcast'] == "true")
	context['NotificationCount'] = int(context['NotificationCount']) if int(context['NotificationCount'] )>= 10 else int(context['NotificationCount'])
	context['TheNotification'] = tryGetKwargs("the_notification", '')

	# loading of notes
	note_list = []
	n = dbORM.get_all('Notes')
	for kn, vn in n.items():
		note_list.append(vn)

	note_list.remove({"id": "0", "name": "NULL", "content": "NULL", "timestamp": "NULL", "datestamp": "NULL"})

	context['NotesBase'] = list(reversed(note_list))

	# Lazy loading of users
	users = dbORM.get_all("UserAPRO")
	context['UserList'] = [u for u in users.values() if u['tier'] != 'god' or u['reg_number'] != context['CUser']['reg_number']]

	# Lazy loading of study materials
	context['StudyMaterials'] = study_materials.Materials().all_materials()

	# Lazy loading of user forms
	context['UserForms'] = [f for f in dbORM.get_all("FormAPRO").values() if f['reg_number'] == u['reg_number'] and f['id'] != "0"]
	context['FormID'] = tryGetKwargs("form_id", "None")

	# Components
	context['components'] = {
		"Note100Component": 'Note100-Component'
	}
	context['GetComponent'] = function_pool.getComponent # API for getting component data

	# Dynamic data
	for x, y in kwargs.items():
		context[f'{x}'] = y

	# APRO Connect(TM) Profiles
	try:
		UserN100_email = function_pool.disbandAPROC(u['APRO-Connect-N100'])['auth1']
		print(UserN100_email)
		context['N100Profile'] = dbORM.get_all('UserN100')[f"{function_pool.isFound('UserN100', 'email', UserN100_email)}"]
		# context['N100Profile'] = None

	except:
		context['N100Profile'] = None

	if u['waitlist'] == "not_decided":
		dbORM.update_entry(
		    "UserAPRO", 
		    f"{function_pool.isFound('UserAPRO', 'id', u['id'])}", 
		    encrypt.encrypter(str({
		        "tier": "pro",
		        "subscripton_plan": "month",
		        "subscription_datestamp_start": f"{function_pool.getDateTime()[0]}",
		        "subscription_datestamp_next": f"{function_pool.getNextBillingDate('month')}",
		        "waitlist": "launched"
		    })), 
		    dnd=False
		)
		flash(f"Hey {u['first_name']}, you've been gifted a Voho Pro subscription for one month.", category=['SUC', 'Voho Pro'])
		return redirect(url_for("views.dashboard"))

	template = "admin-dashboard.html" if tryGetKwargs('admin_pass', None) else "dashboard.html"
	return render_template(template, **context)