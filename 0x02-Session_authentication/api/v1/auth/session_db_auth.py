#!/usr/bin/env python3
"""Session database authentication module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import os
import logging


class SessionDBAuth(SessionExpAuth):
    """Session database authentication class"""
    def create_session(self, user_id=None):
        """Creates and stores a new instance of UserSession"""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID based on a Session ID from the database"""
        if session_id is None:
            return None
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if datetime.now() > user_session[0].created_at + \
                timedelta(seconds=self.session_duration):
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_sessions[0].remove()
        return True
