import os
import secrets
from flask import Flask, render_template, redirect, url_for, session, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import text

# 🚀 Debug info for Railway
print("🚀 Booting app.py")
print("🔍 DATABASE_URL:", os.environ.get("DATABASE_URL"))

# ⚙️ Flask App Init
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']  # 🔐 MUST be set in Railway variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 🔎 Version context
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
    __tablename__ = "user"
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

class Invite_Code(db.Model):
    __tablename__ = "invite_code"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime, nullable=True)
    used_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# 🛡️ Auth Helpers
def current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None

def require_login(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user():
            return redirect(url_for('disclaimer'))
        return f(*args, **kwargs)
    return decorated

def require_admin(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()
        if not user or not user.is_admin:
            return render_template("unauthorized.html")
        return f(*args, **kwargs)
    return decorated

# 🌐 Routes
@app.route("/")
def index():
    return render_template("disclaimer.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.check_password(request.form["password"]):
            session["user_id"] = user.id
            user.last_ip = request.remote_addr
            user.user_agent = request.headers.get('User-Agent')
            db.session.commit()
            flash("Connexion réussie", "success")
            return redirect(url_for("menu"))
        else:
            flash("Identifiants invalides", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(username=request.form["username"]).first():
            flash("Ce pseudo est déjà pris.", "danger")
            return redirect(url_for("register"))
        invite = InviteCode.query.filter_by(code=request.form["invite_code"]).first()
        if not invite:
            flash("Code d'invitation invalide.", "danger")
            return redirect(url_for("register"))
        new_user = User(
            username=request.form["username"],
            level=1, prestige=0, is_admin=False,
            invite_code=request.form["invite_code"])
        new_user.set_password(request.form["password"])
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie, connecte-toi !", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Déconnecté.", "info")
    return redirect(url_for("disclaimer"))

@app.route("/menu")
@require_login
def menu():
    user = current_user()
    return render_template("menu.html", user=user)

@app.route("/missions")
@require_login
def missions():
    user = current_user()
    return render_template("missions.html", user=user)

@app.route("/boutique")
@require_login
def boutique():
    user = current_user()
    return render_template("boutique.html", user=user)

@app.route("/don", methods=["GET", "POST"])
@require_login
def don():
    user = current_user()
    if request.method == "POST":
        montant = int(request.form["montant"])
        user.donations += montant
        user.money -= montant
        db.session.commit()
        flash(f"Merci pour ton don de {montant}€ !", "success")
    return render_template("don.html", user=user)

@app.route("/offrandes")
@require_login
def offrandes():
    user = current_user()
    return render_template("offrandes.html", user=user)

@app.route("/statistique")
@require_login
def statistique():
    user = current_user()
    return render_template("statistique.html", user=user)

@app.route("/dashboard")
@require_admin
def dashboard():
    users = User.query.all()
    invites = InviteCode.query.all()
    stats = {
        "user_count": User.query.count(),
        "level_avg": round(db.session.query(db.func.avg(User.level)).scalar() or 1, 1),
        "prestige_total": db.session.query(db.func.sum(User.prestige)).scalar() or 0,
    }
    return render_template(
        "dashboard.html",
        user=current_user(),
        users=users,
        invites=invites,
        stats=stats
    )

@app.route("/generate_invite", methods=["POST"])
@require_admin
def generate_invite():
    code = secrets.token_hex(8)
    new_invite = InviteCode(code=code, created_by=current_user().id)
    db.session.add(new_invite)
    db.session.commit()
    flash(f"Code généré : {code}", "success")
    return redirect(url_for("dashboard"))

@app.route("/delete_user/<int:user_id>", methods=["POST"])
@require_admin
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username == "Topaz":
        flash("Impossible de supprimer le demi-dieu !", "danger")
        return redirect(url_for("dashboard"))
    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé.", "info")
    return redirect(url_for("dashboard"))

# 🧪 Health Check
@app.route("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ DB connected!", 200
    except Exception as e:
        return f"❌ DB error: {str(e)}", 500

# 🛑 Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def unauthorized(e):
    return render_template('unauthorized.html'), 401

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# 🎯 Local run fallback
if __name__ == "__main__":
    app.run(debug=True)
