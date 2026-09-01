"""
Quick helper: signs up a brand new test user and prints the token +
user_id, ready to paste into test_full_pipeline.py.
"""
import requests

resp = requests.post(
    "http://127.0.0.1:8000/auth/signup",
    json={"email": "freshtoken@example.com", "password": "TestPass123"},
)

if resp.status_code != 200:
    print("Signup failed, trying login instead (email may already exist)...")
    resp = requests.post(
        "http://127.0.0.1:8000/auth/login",
        json={"email": "freshtoken@example.com", "password": "TestPass123"},
    )

data = resp.json()
print("user_id =", data.get("user_id"))
print("access_token =", data.get("access_token"))