"""
Reliable test script for endpoints requiring the authorization header.
Swagger's /docs UI has been unreliable with header fields - this sidesteps
that entirely using the same approach that worked for /projects/ earlier.
"""
import requests

BASE_URL = "http://127.0.0.1:8000"

ACCESS_TOKEN = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjlkMjVhMzdhLWM4YzMtNDVhMy04OWIyLTExZDk4Y2RmODk4MCIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3B4bnFod2lxcG5mZW1kZ3NmdGx4LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJmY2Y0YmVlYy0zN2VmLTQ3OTgtYjI2My1jNGQ2ZWRkZThlZjciLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg4MjkxMDA4LCJpYXQiOjE3ODgyODc0MDgsImVtYWlsIjoiZnJlc2h0b2tlbkBleGFtcGxlLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJmcmVzaHRva2VuQGV4YW1wbGUuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiZmNmNGJlZWMtMzdlZi00Nzk4LWIyNjMtYzRkNmVkZGU4ZWY3In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3ODgyODc0MDh9XSwic2Vzc2lvbl9pZCI6IjE2NDM0ZjVlLWQwMjQtNDEzMi1iYWRkLTY3Y2U0NWYwYWEwMyIsImlzX2Fub255bW91cyI6ZmFsc2V9.0d72ElSo_16uV02JsfY5Aen7PVUI_eXszvd3_BfaJbp83lj0uPZFwlIlLJeby2oPKJOM7uAy1AZ6-4Ut89kU0Q"
USER_ID = "fcf4beec-37ef-4798-b263-c4d6edde8ef7"

HEADERS = {
    "Content-Type": "application/json",
    "authorization": f"Bearer {ACCESS_TOKEN}",
}

# ---- Step 1: create a project ----
print("=== Creating project ===")
project_resp = requests.post(
    f"{BASE_URL}/projects/",
    headers=HEADERS,
    json={
        "user_id": USER_ID,
        "name": "Matcha Cafe Identity",
        "brief_text": "Create a premium visual identity for a modern matcha cafe aimed at young professionals.",
        "project_type": "Branding",
        "target_audience": "Young professionals",
        "desired_mood": "Calm, modern, feminine, playful",
    },
)
print("Status:", project_resp.status_code)
print(project_resp.json())

if project_resp.status_code != 200:
    print("Stopping - project creation failed.")
    exit()

project_id = project_resp.json()["id"]
print("\nproject_id:", project_id)

# ---- Step 2: save a board for this project ----
print("\n=== Saving board ===")
board_resp = requests.put(
    f"{BASE_URL}/boards/{project_id}",
    headers=HEADERS,
    json={
        "elements": [
            {"type": "image", "ref": "img1", "x": 40, "y": 40, "w": 360, "h": 480},
            {"type": "swatch", "color": "#F3A7B6", "x": 40, "y": 540, "w": 360, "h": 220},
            {"type": "text", "content": "Sun-Drenched Pastel Editorial", "x": 420, "y": 40, "w": 360, "h": 180},
        ]
    },
)
print("Status:", board_resp.status_code)
print(board_resp.json())

# ---- Step 3: submit feedback ----
print("\n=== Submitting feedback ===")
feedback_resp = requests.post(
    f"{BASE_URL}/feedback/",
    headers=HEADERS,
    json={
        "project_id": project_id,
        "output_type": "direction",
        "rating": "up",
        "comment": "Love this palette",
    },
)
print("Status:", feedback_resp.status_code)
print(feedback_resp.json())

# ---- Step 4: export the project ----
print("\n=== Exporting project ===")
export_resp = requests.get(f"{BASE_URL}/export/{project_id}", headers=HEADERS)
print("Status:", export_resp.status_code)
print(export_resp.text[:500], "...")