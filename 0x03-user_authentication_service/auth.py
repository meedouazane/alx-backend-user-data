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
