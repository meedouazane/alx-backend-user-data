#!/usr/bin/env python3
""" Sessions in database """
from models.base import Base


def UserSession(Base):
    """ Sessions in database """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
