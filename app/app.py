#testing
from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Asseiment 3</title>
    <style>
        body { font-family: sans-serif; margin: 30px; background: #f7f7f7; }
        h1 { color: #333; }
        textarea, input { width: 100%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; background: #007BFF; color: white; border: none; }
        pre { background: #eee; padding: 10px; }
    </style>
</head>
<body>
    <h1>Flask API</h1>
    <p><strong>POST /add</strong> – Add text</p>
    <input type="text" id="dataInput" placeholder="writing...">
    <button onclick="postData()">Add</button>

    <p><strong>GET /entries</strong> – Show</p>
    <button onclick="loadEntries()">Show entries</button>

    <pre id="result"></pre>

<script>
    function postData() {
        fetch('/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: document.getElementById('dataInput').value })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        });
    }

    function loadEntries() {
        fetch('/entries')
        .then(res => res.json())
        .then(data => {
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        });
    }
</script>
</body>
</html>
"""

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'testdb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )
    return conn

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/add', methods=['POST'])
def add_entry():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO entries (data) VALUES (%s)', (data['data'],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'added'})

@app.route('/entries', methods=['GET'])
def get_entries():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM entries')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
