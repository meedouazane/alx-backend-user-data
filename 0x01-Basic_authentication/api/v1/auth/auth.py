#!/usr/bin/env python3
""" Auth class """
import fnmatch
from typing import TypeVar, List
from flask import request
import fnmatch


class Auth:
    """ class Auth """

    def require_auth(
            self, path: str, excluded_paths: List[str]) -> bool:
        """ public method require auth """
        i = 0
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        for item in excluded_paths:
            if fnmatch.fnmatch(path, item):
                return False
        if path not in excluded_paths:
            return True

    def authorization_header(self, request=None) -> str:
        """ public method require authorization header """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ public method current user """
        return None
