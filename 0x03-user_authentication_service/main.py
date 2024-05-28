#!/usr/bin/env python3
"""
Main file
"""
import requests
from auth import Auth

AUTH = Auth()


def register_user(email: str, password: str) -> None:
    """ Test for register users  """
    payload = {'email': email, 'password': password}
    r = requests.post('http://127.0.0.1:5000/users', data=payload)
    assert r.status_code == 200
    expected = {"email": email, "message": "user created"}
    assert (r.json() == expected)


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test to loging with wrong password """
    payload = {'email': email, 'password': password}
    r = requests.post('http://127.0.0.1:5000/sessions', data=payload)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test for login """
    payload = {'email': email, 'password': password}
    r = requests.post('http://127.0.0.1:5000/sessions', data=payload)
    print(r.status_code)
    assert r.status_code == 200
    expected = {"email": email, "message": "logged in"}
    assert (r.json() == expected)
    return r.cookies.get('session_id')



def profile_unlogged() -> None:
    """ """

def profile_logged(session_id: str) -> None:
    """ """
def log_out(session_id: str) -> None:
    """ """
def reset_password_token(email: str) -> str:
    """ """

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ """


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
