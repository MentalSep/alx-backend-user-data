#!/usr/bin/python3
"""Main file"""
import requests

BASE_URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    body = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/users", data=body)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    body = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=body)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    body = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=body)
    assert response.status_code == 200
    return response.json()["message"]


def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    body = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", data=body)
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    body = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(f"{BASE_URL}/reset_password", data=body)
    assert response.status_code == 200


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
