#!/usr/bin/env python3
"""  handles all routes for the Session authentication. """
from api.v1.views import app_views
from flask import request, jsonify
from os import getenv
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def Session_auth():
    """ handles routes for the Session authentication """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 401
    if not password:
        return jsonify({"error": "password missing"}), 401
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password) is False:
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        c_session = auth.create_session(user.id)
        response = jsonify(user.to_json())
        session_name = getenv('SESSION_NAME')
        response.set_cookie(session_name, c_session)
    return response
