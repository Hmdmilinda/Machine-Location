from flask import Flask, request, render_template_string, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheet setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"  # <-- your downloaded JSON file
SHEET_NAME = "App_Data"

# Connect to Google Sheet
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# HTML template
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Entry App</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f9f9f9; }
        form { background: white; padding: 20px; border-radius: 10px; width: 300px; margin-bottom: 30px; }
        input, button { padding: 8px; margin: 5px 0; width: 100%; }
        table { border-collapse: collapse; width: 60%; background: white; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background: #007BFF; color: white; }
    </style>
</head>
<body>
    <h2>📋 Data Entry (Google Sheet)</h2>
    <form method="POST" action="/add">
        <input type="text" name="text" placeholder="Enter text" required>
        <input type="number" name="number" placeholder="Enter number" required>
        <button type="submit">Submit</button>
    </form>

    <h3>Stored Data:</h3>
    <table>
        <tr><th>Text</th><th>Number</th></tr>
        {% for row in data %}
        <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    data = sheet.get_all_values()[1:]  # skip header
    return render_template_string(HTML, data=data)

@app.route('/add', methods=['POST'])
def add():
    text = request.form['text']
    number = request.form['number']
    sheet.append_row([text, number])
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
