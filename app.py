
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2, os

app = Flask(__name__)
app.secret_key = 'eclipse_pgsql_secret'

def get_db():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        code = request.form['invite_code']
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM invites WHERE code = %s AND used = FALSE', (code,))
        invite = cur.fetchone()
        if invite:
            if username.lower() == 'topaz':
                return 'Ce nom est réservé.'
            hashed = generate_password_hash(password)
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed))
            cur.execute('UPDATE invites SET used = TRUE, used_by = %s WHERE code = %s', (username, code))
            db.commit()
            cur.close()
            return redirect(url_for('login'))
        return 'Code invalide ou déjà utilisé.'
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return 'Identifiants incorrects.'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
