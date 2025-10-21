from flask import Flask, request, render_template_string

app = Flask(__name__)

# Temporary in-memory storage (just for testing)
data_storage = []

# Home route - displays the form
@app.route('/')
def home():
    return render_template_string("""
        <html>
        <head>
            <title>📊 Data Entry App</title>
            <style>
                body { font-family: Arial; text-align: center; margin-top: 100px; }
                input, button { padding: 10px; margin: 5px; }
                button { background-color: #4CAF50; color: white; border: none; }
            </style>
        </head>
        <body>
            <h2>📊 Data Entry App</h2>
            <form method="POST" action="/submit">
                <input name="text_input" placeholder="Enter text" required>
                <input name="number_input" type="number" placeholder="Enter number" required>
                <button type="submit">Submit</button>
            </form>
            <br>
            <a href="/data">📄 View Submitted Data</a>
        </body>
        </html>
    """)

# Submit route - handles form data
@app.route('/submit', methods=['POST'])
def submit():
    text_value = request.form['text_input']
    number_value = request.form['number_input']

    # Store in memory for now
    data_storage.append({'text': text_value, 'number': number_value})
    print("Data received:", text_value, number_value)

    return f"""
        ✅ Data Saved Successfully!<br><br>
        Text: {text_value}<br>
        Number: {number_value}<br><br>
        <a href='/'>Go Back</a> | <a href='/data'>View All Data</a>
    """

# Route to view all stored data
@app.route('/data')
def view_data():
    if not data_storage:
        return "<h3>No data submitted yet.</h3><a href='/'>Go Back</a>"

    rows = "".join([f"<tr><td>{d['text']}</td><td>{d['number']}</td></tr>" for d in data_storage])
    return f"""
        <h2>📋 Submitted Data</h2>
        <table border='1' cellpadding='8' style='margin:auto;'>
            <tr><th>Text</th><th>Number</th></tr>
            {rows}
        </table>
        <br><a href='/'>Go Back</a>
    """

# Run Flask app on Replit environment
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
