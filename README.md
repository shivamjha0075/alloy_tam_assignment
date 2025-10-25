# Alloy Evaluation API

A Python application that integrates with the Alloy API for identity verification and risk assessment. This project includes both a command-line script and a modern web interface for submitting and processing applications.



## 🛠️ Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```env
WORKFLOW_TOKEN=your_workflow_token_here
WORKFLOW_SECRET=your_workflow_secret_here
```

## 🖥️ Usage

### Web Interface
1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Fill out the application form and submit

### Command Line Script
```bash
python script.py
```

### Required Fields
- **Name**: First and last name
- **Date of Birth**: YYYY-MM-DD format
- **SSN**: Exactly 9 digits
- **Email**: Valid email address
- **Address**: Complete address information
