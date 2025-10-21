from flask import Flask, request, render_template_string, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
app = Flask(__name__)
# Google Sheet setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"  # <-- your downloaded JSON file
SHEET_NAME = "App_Data"
# Google Sheet setup - using environment variable for credentials
SHEET_NAME = os.environ.get("GOOGLE_SHEET_NAME", "App_Data")
# Connect to Google Sheet
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1
# Initialize sheet connection (will be set up after credentials are provided)
sheet = None
def init_google_sheet():
    """Initialize Google Sheet connection from environment credentials"""
    global sheet
    try:
        creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if not creds_json:
            print("Warning: GOOGLE_CREDENTIALS_JSON not set. Google Sheets features will be unavailable.")
            return False
        
        creds_dict = json.loads(creds_json)
        client = gspread.service_account_from_dict(creds_dict)
        sheet = client.open(SHEET_NAME).sheet1
        return True
    except Exception as e:
        print(f"Error initializing Google Sheet: {e}")
        return False
# HTML template
HTML = """
-0
+4
        table { border-collapse: collapse; width: 60%; background: white; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background: #007BFF; color: white; }
        .error { color: red; padding: 20px; background: #ffe6e6; border-radius: 5px; }
    </style>
</head>
<body>
    <h2>📋 Data Entry (Google Sheet)</h2>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% else %}
    <form method="POST" action="/add">
        <input type="text" name="text" placeholder="Enter text" required>
        <input type="number" name="number" placeholder="Enter number" required>
-7
+29
        <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td></tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
"""
@app.route('/')
def index():
    data = sheet.get_all_values()[1:]  # skip header
    return render_template_string(HTML, data=data)
    if sheet is None:
        return render_template_string(HTML, error="Google Sheets not configured. Please set up credentials.", data=[])
    try:
        data = sheet.get_all_values()[1:]  # skip header
        return render_template_string(HTML, data=data, error=None)
    except Exception as e:
        return render_template_string(HTML, error=f"Error reading sheet: {e}", data=[])
@app.route('/add', methods=['POST'])
def add():
    text = request.form['text']
    number = request.form['number']
    sheet.append_row([text, number])
    return redirect('/')
    if sheet is None:
        return render_template_string(HTML, error="Google Sheets not configured. Please set up credentials.", data=[])
    try:
        text = request.form['text']
        number = request.form['number']
        sheet.append_row([text, number])
        return redirect('/')
    except Exception as e:
        return render_template_string(HTML, error=f"Error adding data: {e}", data=[])
@app.after_request
def add_header(response):
    """Add cache control headers for Replit proxy compatibility"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
if __name__ == '__main__':
    app.run(debug=True)
    # Initialize Google Sheet connection
    init_google_sheet()
    # Run on 0.0.0.0:5000 for Replit compatibility
    app.run(host='0.0.0.0', port=5000, debug=True)
