from flask import Flask, request, redirect, render_template, send_file
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from api.models import db, AdminUser, ADMIN_CREDENTIALS
from api.routes.hidden_gems import hidden_gems_bp
from api.routes.planner import planner_bp  # if you've added trip planner API

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # 🔐 Change this in production
CORS(app)

# Initialize DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wandermap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Load user from session
@login_manager.user_loader
def load_user(user_id):
    return AdminUser(user_id)

# Register Blueprints
app.register_blueprint(hidden_gems_bp)
app.register_blueprint(planner_bp)  # Only if you created planner.py

# --------------------------------
# 🔐 ADMIN LOGIN / LOGOUT ROUTES
# --------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            user = AdminUser(username)
            login_user(user)
            return redirect('/admin')
        else:
            return "❌ Invalid username or password", 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# --------------------------------
# 🔐 ADMIN DASHBOARD PAGE
# --------------------------------
@app.route('/admin')
@login_required
def admin_page():
    return send_file('admin.html')


# --------------------------------
# ✅ HOME TEST ROUTE (Optional)
# --------------------------------
@app.route('/')
def home():
    return "✅ WanderMap Flask backend is running!"

# -------------------------------
# 🏁 Run the App (Dev Only)
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
