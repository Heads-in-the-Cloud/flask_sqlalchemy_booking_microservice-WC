# from flask import Flask, jsonify
# from utopia import app
# from datetime import datetime, time
# from sqlalchemy.exc import IntegrityError, OperationalError
# from werkzeug.exceptions import NotFound, BadRequest
# from sqlalchemy.orm.exc import UnmappedInstanceError

# @app.errorhandler(Exception)
# def server_error(e):

#     timestamp = datetime.now()

#     print(type(e))
#     NOT_FOUND = 'NOT FOUND'
#     BAD_REQUEST = 'BAD REQUEST'

#     attribute_error = 'One or more primary keys not valid'
#     key_error = 'Missing one or more required fields'
#     integrity_error = 'One or more fields must reference another primary key'
#     value_error = 'Incorrect value type. Check fields in request body'
#     missing_body = 'Missing or invalid request body'
#     missing_path = 'Missing path endpoint'

#     if isinstance(e, (AttributeError, UnmappedInstanceError)):
#         return jsonify({'timestamp' : timestamp, 'message' : attribute_error, 'status' : NOT_FOUND}), 404

#     if isinstance(e, KeyError):
#         return jsonify({'timestamp' : timestamp, 'message' : key_error, 'status': BAD_REQUEST}), 400

#     if isinstance(e, IntegrityError):
#         return jsonify({'timestamp' : timestamp, 'message' : integrity_error, 'status': BAD_REQUEST}), 400

#     if isinstance(e, (ValueError, OperationalError)):
#         return jsonify({'timestamp' : timestamp, 'message' : value_error, 'status': BAD_REQUEST}), 400
    
#     if isinstance(e, BadRequest):
#         return jsonify({'timestamp' : timestamp, 'message' : missing_body, 'status': BAD_REQUEST}), 400

#     if isinstance(e, NotFound):
#             return jsonify({'timestamp' : timestamp, 'message' : missing_path, 'status': BAD_REQUEST}), 400

#     return "something went wrong"