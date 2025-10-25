import os
import re
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
ALLOY_URL = "https://sandbox.alloy.co/v1/evaluations/"
WORKFLOW_TOKEN = os.getenv("WORKFLOW_TOKEN")
WORKFLOW_SECRET = os.getenv("WORKFLOW_SECRET")

# Validate that environment variables are loaded
if not WORKFLOW_TOKEN or not WORKFLOW_SECRET:
    print("Error: WORKFLOW_TOKEN and WORKFLOW_SECRET must be set in .env file")
    exit(1)


def is_valid_email(email):
    """Validate email format using regex."""
    return re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email)


def submit_to_alloy(applicant_data):
    """Send applicant data to Alloy Sandbox API and return JSON response."""
    try:
        response = requests.post(
            ALLOY_URL,
            auth=HTTPBasicAuth(WORKFLOW_TOKEN, WORKFLOW_SECRET),
            json=applicant_data,
            timeout=10
        )

        if response.status_code == 201:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None


def process_response(result):
    """Interpret the Alloy API response and return formatted result."""
    if not result:
        return {
            "class": "denied",
            "title": "❌ Application Error",
            "message": "Unable to process your application. Please try again later."
        }
    
    outcome = result.get("summary", {}).get("outcome", "")
    
    if outcome == "Approved":
        return {
            "class": "approved",
            "title": "Congratulations!",
            "message": "Congratulations! You are approved."
        }
    elif outcome == "Manual Review":
        return {
            "class": "review",
            "title": "Under Review",
            "message": "Your application is under review. Please wait for further updates."
        }
    elif outcome == "Denied":
        return {
            "class": "denied",
            "title": "Application Denied",
            "message": "Unfortunately, we cannot approve your application at this time."
        }
    else:
        return {
            "class": "review",
            "title": "⚠️ Unexpected Response",
            "message": f"Received unexpected outcome: {outcome}."
        }


@app.route('/')
def index():
    """Display the application form."""
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_application():
    """Handle form submission and process with Alloy API."""
    # Collect form data
    applicant_data = {
        "name_first": request.form.get('name_first', '').strip(),
        "name_last": request.form.get('name_last', '').strip(),
        "birth_date": request.form.get('birth_date', '').strip(),
        "document_ssn": request.form.get('document_ssn', '').strip(),
        "email_address": request.form.get('email_address', '').strip(),
        "address_line_1": request.form.get('address_line_1', '').strip(),
        "address_city": request.form.get('address_city', '').strip(),
        "address_state": request.form.get('address_state', '').strip(),
        "address_postal_code": request.form.get('address_postal_code', '').strip(),
        "address_country_code": request.form.get('address_country_code', 'US').strip()
    }
    
    # Basic validation
    if not all(applicant_data.values()):
        result = {
            "class": "denied",
            "title": "❌ Validation Error",
            "message": "Please fill in all required fields."
        }
        return render_template('index.html', result=result)
    
    # Validate SSN format (exactly 9 digits)
    if not re.match(r'^\d{9}$', applicant_data['document_ssn']):
        result = {
            "class": "denied",
            "title": "❌ Invalid SSN",
            "message": "Social Security Number must be exactly 9 digits (no spaces or dashes)."
        }
        return render_template('index.html', result=result)
    
    # Validate email format
    if not is_valid_email(applicant_data['email_address']):
        result = {
            "class": "denied",
            "title": "❌ Invalid Email",
            "message": "Please enter a valid email address."
        }
        return render_template('index.html', result=result)
    
    # Submit to Alloy API
    api_response = submit_to_alloy(applicant_data)
    result = process_response(api_response)
    
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)