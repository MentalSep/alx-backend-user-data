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
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path[-1] != '/':
                path += '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request
        """
        return None
