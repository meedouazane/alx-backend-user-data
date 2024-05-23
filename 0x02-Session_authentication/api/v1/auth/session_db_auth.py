#!/usr/bin/env python3
""" Sessions in database """
from api.v1.auth.session_auth import SessionAuth
from models.user_session import UserSession


class SessionDBAuth(SessionAuth):
    """ inherits from SessionExpAuth """

    def create_session(self, user_id=None):
        """ Overload of create_session """
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        attr = {
            "user_id": user_id,
            "session_id": sess_id
        }
        user = UserSession(**attr)
        user.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ Overload Of user_id_for_session_id """
        user_id = UserSession.search({"session_id": session_id})
        if not user_id:
            return None
        return user_id

    def destroy_session(self, request=None):
        """ destroys the UserSession based on the Session ID  """
        if not request:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_sess = UserSession.search({"session_id": sess_id})
        if user_sess:
            user_sess[0].remove()
            return True
        return False
