import mysql.connector
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'temporary_key'

def get_db_connection():
    return mysql.connector.connect(
        host='clonedb.cnqego2u43e5.ap-south-1.rds.amazonaws.com',
        user='admin',
        password='hailamazonrds',
        database='clone_db'
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (%s, %s)',
            (username, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        password = request.form['password']
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and check_password_hash(result[0], password):
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')


# Dashboard Route (after login)
@app.route('/dashboard')
def dashboard():
    course_urls = [
        'https://clonebucket0.s3.ap-south-1.amazonaws.com/UNIT+4.pdf',
        'https://clonebucket0.s3.ap-south-1.amazonaws.com/UNIT+5.pdf'
    ]
    return render_template('dashboard.html', course_urls=course_urls)

# Home Route (Landing Page)

@app.route('/')
def home():
    return render_template('home.html')


# Logout

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)