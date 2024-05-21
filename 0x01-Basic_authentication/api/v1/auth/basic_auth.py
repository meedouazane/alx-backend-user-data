#!/usr/bin/env python3
""" Basic auth """
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User
from models.base import Base


class BasicAuth(Auth):
    """ class BasicAuth that inherits from Auth """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if (authorization_header is None or
                type(authorization_header) is not str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.replace('Basic ', '')

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64
        string base64_authorization_header
        """
        if (base64_authorization_header is None
                or type(base64_authorization_header) is not str):
            return None
        try:
            encoded_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or
                type(decoded_base64_authorization_header) is not str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':', 1)
        if len(credentials) != 2:
            return None
        email, password = credentials
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password."""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd) is False:
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth = Auth.authorization_header(request)
        if not auth:
            return None
        extract = self.extract_base64_authorization_header(auth)
        if not extract:
            return None
        decode = self.decode_base64_authorization_header(extract)
        if not decode:
            return None
        email, password = self.extract_user_credentials(decode)
        if not email or not password:
            return None
        user = self.user_object_from_credentials(email, password)
        if not user:
            return None
        return user
