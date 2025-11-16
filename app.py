# app.py
from flask import Flask
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask import redirect, request, url_for
import jwt

from models import db, User, Course, Enrollment
from routes import routes  

app = Flask(__name__)
from flask_cors import CORS

CORS(app)


# CONFIG

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"   
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"  


# INITIALIZE DATABASE

db.init_app(app)

with app.app_context():
    db.create_all()

# REGISTER BLUEPRINT ROUTES

app.register_blueprint(routes)


# FLASK ADMIN (ADMIN INTERFACE)

admin = Admin(app, name="ACME Admin")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Enrollment, db.session))

class AdminSecureModelView(ModelView):
    def is_accessible(self):
        if request.method == "OPTIONS":
            return True  # Allow preflight
        token = request.cookies.get("token") or request.headers.get("Authorization")
        if not token:
            return False
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            return data.get("role") == "admin"
        except Exception:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/static/login.html")


# RUN SERVER

if __name__ == "__main__":
    app.run(debug=True, port=3000)
