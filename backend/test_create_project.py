"""
Quick manual test script for POST /projects/.
Run with: python test_create_project.py
"""
import requests

# paste your real access_token here (from /auth/signup or /auth/login)
ACCESS_TOKEN = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjlkMjVhMzdhLWM4YzMtNDVhMy04OWIyLTExZDk4Y2RmODk4MCIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3B4bnFod2lxcG5mZW1kZ3NmdGx4LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJiNTYwOWQwMC1mNzk1LTQ0NGUtYTY1Yy1iYjMxNjNiZjZkN2YiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg3NzM5NjM4LCJpYXQiOjE3ODc3MzYwMzgsImVtYWlsIjoibm14ZGVzaWduczFAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im5teGRlc2lnbnMxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6ImI1NjA5ZDAwLWY3OTUtNDQ0ZS1hNjVjLWJiMzE2M2JmNmQ3ZiJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzg3NzM2MDM4fV0sInNlc3Npb25faWQiOiJlOTZhOWIzNS03ZTlkLTQwM2MtYTQ2My02YTU1OTdmYmM3OTYiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.rxkigaX_AswVbJJFPovrAM2upU7NklGH4mR2jQ7Njg5BB89DOT8jOYd3YrmKYbw26aN_OvA3BXtqqoQaAy9niA"
USER_ID = "b5609d00-f795-444e-a65c-bb3163bf6d7f"

response = requests.post(
    "http://127.0.0.1:8000/projects/",
    headers={
        "Content-Type": "application/json",
        "authorization": f"Bearer {ACCESS_TOKEN}",
    },
    json={
        "user_id": USER_ID,
        "name": "Matcha Cafe Identity",
        "brief_text": "Create a premium visual identity for a modern matcha cafe aimed at young professionals. I want it to feel calm, modern, feminine, Japanese-inspired, and slightly playful.",
        "project_type": "Branding",
        "target_audience": "Young professionals",
        "desired_mood": "Calm, modern, feminine, playful",
    },
)

print("Status code:", response.status_code)
print("Response body:", response.json())