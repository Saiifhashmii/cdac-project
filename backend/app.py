from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('POSTGRES_DB', 'bugdb'),
        user=os.getenv('POSTGRES_USER', 'user'),
        password=os.getenv('POSTGRES_PASSWORD', 'pass')
    )

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

