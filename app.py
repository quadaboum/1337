import os
import secrets
from flask import Flask, render_template, redirect, url_for, session, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import text

# 🔍 Debug output for Railway
print("🚀 Booting app.py")
print("🔍 DATABASE_URL:", os.environ.get("DATABASE_URL"))

# 🔐 App init
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# 💣 Validate DB URI
uri = os.environ.get("DATABASE_URL")
if not uri:
    raise RuntimeError("❌ DATABASE_URL not set in environment!")
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 🔎 Version injection
def get_version():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except Exception:
        return "?"

@app.context_processor
def inject_version():
    return {"version": get_version()}

# 🧬 Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, default=1)
    prestige = db.Column(db.Integer, default=0)
    last_ip = db.Column(db.String(100))
    user_agent = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    money = db.Column(db.Integer, default=0)
    invite_code = db.Column(db.String(16), unique=True)
    donations = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class InviteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

# 🔒 Auth helpers
def current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None

@app.route("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ DB connected!", 200
    except Exception as e:
        return f"❌ DB error: {str(e)}", 500
if __name__ == "__main__":
    app.run(debug=True)
