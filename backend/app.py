from flask import Flask, render_template, request, redirect
import psycopg2
import os

# 📊 Prometheus client imports
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 📊 Define Prometheus metrics
REQUEST_COUNT = Counter(
    'flask_http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint']
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'bugtracker'),
        user=os.getenv('POSTGRES_USER', 'admin'),
        password=os.getenv('POSTGRES_PASSWORD', 'pass')
    )

@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

# ✅ Fix for / route
@app.route('/')
def home():
    return render_template('submit.html')

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    description = request.form['description']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO bugs (title, description) VALUES (%s, %s);", (title, description))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/bugs')

@app.route('/bugs')
def bugs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bugs;")
    bugs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('bugs.html', bugs=bugs)

# 📊 Metrics endpoint for Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

