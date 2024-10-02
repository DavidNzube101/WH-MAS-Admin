# # from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
# # from flask_login import login_required, current_user
# # from werkzeug.utils import secure_filename


# # # from datetime import datetime
# # from datetime import datetime, timedelta
# # import base64
# # import random
# # import imghdr
# # import json
# # import datetime as dt

# # from . import DateToolKit as dtk
# # from . import function_pool
# # from . import ScreenGoRoute
# # from . import id_generator

# # from .SarahDBClient.db import db
# # from .SarahDBClient.db import dbORM
# # from .SarahDBClient import encrypt


# # ----------------------------------Sample from client_actions.py-----------------------------s
from flask import Blueprint, render_template, current_app, request, jsonify
import firebase_admin
# from firebase_admin import credentials, firestore
from flask_login import login_required, current_user
from . import DateToolKit as dtk
from . import function_pool
# from .SarahDBClient.SarahClient import dbORM
# import asyncio
# from functools import wraps

client_actions2 = Blueprint('client_actions2', __name__)
ca = client_actions2

# cred = credentials.Certificate('website/SarahDBClient/voho-backend-service-firebase-adminsdk-5wbds-ce771015c4.json')
# firebase_admin.initialize_app(cred)

# db = firestore.client()


@ca.route("/assignment/open/thread/<string:assignment_id>")
@login_required
def renderAddSolution(assignment_id):

    context = {
        'Assignment': assignment,
        'CUser': user,
        'getMIME': function_pool.get_mime_type,
        'DTK': dtk,
        'GetOppositeVisibility': function_pool.GetOppositeVisibility,
        'Solutions': solutions,
        'DBORM': function_pool.dbORMJinja,
        'GetReviewCount': function_pool.getReviewCount,
        'ShortenText': function_pool.shorten_text
    }
    
    return render_template("AssignmentThread.html", **context)

@ca.route("/assignment/open/thread/<string:assignment_id>/solution/<string:solution_id>")
@login_required
def renderSolutionThread(assignment_id, solution_id):

    context = {
        'Assignment': assignment,
        'CUser': user,
        'getMIME': function_pool.get_mime_type,
        'DTK': dtk,
        'GetOppositeVisibility': function_pool.GetOppositeVisibility,
        'Solutions': solutions,
        'DBORM': function_pool.dbORMJinja,
        'GetReviewCount': function_pool.getReviewCount,
        'ShortenText': function_pool.shorten_text
    }

    return render_template("SolutionThread.html", **context)



# @app.route('/add', methods=['POST'])
# def add_document():
#     data = request.get_json()
#     # Add a new document to the "users" collection
#     doc_ref = db.collection('users').add(data)
#     return jsonify({"id": doc_ref.id}), 200

# @app.route('/get/<doc_id>', methods=['GET'])
# def get_document(doc_id):
#     doc_ref = db.collection('users').document(doc_id)
#     doc = doc_ref.get()
#     if doc.exists:
#         return jsonify(doc.to_dict()), 200
#     else:
#         return jsonify({"error": "Document not found"}), 404

# @app.route('/update/<doc_id>', methods=['PUT'])
# def update_document(doc_id):
#     data = request.get_json()
#     doc_ref = db.collection('users').document(doc_id)
#     doc_ref.update(data)
#     return jsonify({"status": "Document updated"}), 200

# @app.route('/delete/<doc_id>', methods=['DELETE'])
# def delete_document(doc_id):
#     doc_ref = db.collection('users').document(doc_id)
#     doc_ref.delete()
#     return jsonify({"status": "Document deleted"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)
