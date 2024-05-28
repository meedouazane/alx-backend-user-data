#!/usr/bin/env python3
"""
Authentication moduel for user
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from user import User
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register user
        :param email: email of user
        :param password: password of user
        :return: User User object
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Credentials validation
        :param email: email of user
        :param password: password of user
        :return: User User object
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Get session ID
        :param email: email of user
        :return: session id of user
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Find user by session ID
        :param session_id: session id of user
        :return: User object
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy session
        :param user_id: id of user
        :return: None
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate reset password token
        :param email: email of user
        :return: Return the token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        uuid_gen = _generate_uuid()
        self._db.update_user(user.id, reset_token=uuid_gen)
        return uuid_gen

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update password
        :param reset_token: user reset token
        :param password: user password
        :return: None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed, reset_token=None)


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments and returns bytes.
    Args:
        password: password from user
    Return:
         hashed password
    """
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byte, salt)


def _generate_uuid(self) -> str:
    """
    Generate string representation of a new UUID
    Return:
        string representation of a new UUID
    """
    return str(uuid4())
