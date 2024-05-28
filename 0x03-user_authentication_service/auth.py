#!/usr/bin/env python3
""" 
Authentication module for user 
"""
import bcrypt
from sqlalchemy.exc import NoResultFound
import uuid
from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """ Creates password hash
        Args:
            - password: user password
        Return:
            - hashed password
    """
    e_pwd = password.encode()
    return bcrypt.hashpw(e_pwd, bcrypt.gensalt())
