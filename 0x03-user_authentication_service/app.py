#!/usr/bin/env python3
""" Flask app """
from flask import (Flask, jsonify,
                   request, abort, make_response, redirect)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def route() -> str:
    """
    first route Basic Flask app
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """
    Register user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Log in function
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if session_id:
        response = make_response(jsonify({
            "email": f"{email}",
            "message": "logged in"
        }))
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Log out function
    """
    sess_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    User profile
    """
    sess_id = request.cookies.get("session_id")
    if sess_id:
        user = AUTH.get_user_from_session_id(sess_id)
        if user:
            return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Get reset password token
    """
    email = request.form.get("email")
    if email:
        reset_token = AUTH.get_reset_password_token(email)
        if reset_token:
            return jsonify({
                "email": f"{email}",
                "reset_token": f"{reset_token}"
            }), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def update_password():
    """ Update password end-point """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    password = request.form.get("password")
    try:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": f"{email}",
                        "message": "Password updated"
                        }), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
