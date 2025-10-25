import requests
from requests.auth import HTTPBasicAuth
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import sys 
import json

# ---------------------------
# Alloy TAM Work Assignment
# Author: Shivam Jha
# ---------------------------

# --- Configuration ---
ALLOY_URL = "https://sandbox.alloy.co/v1/evaluations/"
WORKFLOW_TOKEN = os.getenv("WORKFLOW_TOKEN")
WORKFLOW_SECRET = os.getenv("WORKFLOW_SECRET")

# Validate that environment variables are loaded
if not WORKFLOW_TOKEN or not WORKFLOW_SECRET:
    print("Error: WORKFLOW_TOKEN and WORKFLOW_SECRET must be set in .env file")
    exit(1)

# --- Applicant Data ---
applicant_data = {
    "name_first": "Shivam",
    "name_last": "Approved",  # Change to "Deny" or any other name to test
    "birth_date": "1990-05-15",
    "document_ssn": "123456789",
    "email_address": "shivam@test.com",
    "address_line_1": "123 Main St",
    "address_city": "San Jose",
    "address_state": "CA",
    "address_postal_code": "95122",
    "address_country_code": "US"
}

# --- Make API Request ---
response = requests.post(
    ALLOY_URL,
    auth=HTTPBasicAuth(WORKFLOW_TOKEN, WORKFLOW_SECRET),
    json=applicant_data
)

# --- Process Response ---
if response.status_code == 201:
    data = response.json()
    outcome = data.get("summary", {}).get("outcome", "")

    if outcome == "Approved":
        print("✅ Congratulations! You are approved.")
        print("Raw Response:", response.status_code, response.text)
    elif outcome == "Manual Review":
        print("🕐 Your application is under review. Please wait for further updates.")
        print("Raw Response:", response.status_code, response.text)
    elif outcome == "Denied":
        print("❌ Unfortunately, we cannot approve your application at this time.")
        print("Raw Response:", response.status_code, response.text)
    else:
        print("⚠️ Unexpected outcome:", outcome)
else:
    print("Error:", response.status_code, response.text)