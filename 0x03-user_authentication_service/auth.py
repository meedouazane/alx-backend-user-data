#!/usr/bin/env python3
""" Hash password """
import bcrypt
from sqlalchemy.exc import NoResultFound
import uuid
from db import DB


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes. """
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """ Register user """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        return user

    def valid_login(self, email, password):
        """ Credentials validation """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def _generate_uuid(self):
        """  return a string representation of a new UUID """
        return str(uuid.uuid4())

    def create_session(self, email):
        """ Get session ID """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = self._generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """ Find user by session ID """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        """ Destroy session """
        if user_id:
            self._db.update_user(user_id, session_id=None)
            return None

    def get_reset_password_token(self, email):
        """ Generate reset password token """
        try:
            user = self._db.find_user_by(email=email)
            uuid_gen = self._generate_uuid()
            return self._db.update_user(user.id, reset_token=uuid_gen)
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token, password):
        """ Update password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed)
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError
