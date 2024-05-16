#!/usr/bin/env python3
"""Module encrypt_password.py"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
