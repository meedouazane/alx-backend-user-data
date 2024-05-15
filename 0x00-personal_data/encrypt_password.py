#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password """
    byt = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byt, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check valid password """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
