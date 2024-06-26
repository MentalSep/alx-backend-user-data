#!/usr/bin/env python3
"""
Session expiration authentication module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    Session Expiration Authentication Class
    """
    def __init__(self):
        """
        Constructor method
        """
        super().__init__()
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """
        Creates a Session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID based on a Session ID with expiration
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_dict.get('user_id')
