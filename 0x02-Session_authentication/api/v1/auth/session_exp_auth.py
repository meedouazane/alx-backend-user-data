#!/usr/bin/env python3
""" Session authentication """
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """  inherits from SessionAuth """

    def __init__(self):
        """ int class """
        try:
            s_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            s_duration == 0
        self.session_duration = s_duration

    def create_session(self, user_id=None):
        """ Overload of create_session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        SessionAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overload Of user_id_for_session_id """
        if session_id is None:
            return None
        session_dic = SessionAuth.user_id_by_session_id.get(session_id)
        if not session_dic:
            return None
        if self.session_duration <= 0:
            return session_dic.get('user_id')
        create_at = session_dic.get('created_at')
        if not create_at:
            return None
        exp = create_at + timedelta(seconds=self.session_duration)
        if exp < datetime.now():
            return None
        return session_dic.get('user_id')
