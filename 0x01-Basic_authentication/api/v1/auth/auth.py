#!/usr/bin/env python3
"""
Auth class for authentication system
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if the path requires authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request
        """
        return None
