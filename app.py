from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Helper functions
def hash_password(password):
    if not password:
        raise ValueError("Password cannot be None or empty")
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    if not username or not password:
        return False  #missing input
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[0] == hash_password(password):
        return True
    return False

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('Home-Page.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        
        if check_user(username, password):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials!", 401
    
    return render_template('Login-Register.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        password = hash_password(password)
    
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            conn.close()
            session['user'] = username
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            conn.close()
            return "User already exists!", 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
