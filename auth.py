# auth.py
import datetime, jwt
from flask import request, jsonify
from functools import wraps

SECRET = "SUPER_SECRET_KEY"

def generate_token(user):
    return jwt.encode({
        "id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET, algorithm="HS256")

def auth_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Missing token"}), 401

            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            try:
                data = jwt.decode(token, SECRET, algorithms=["HS256"])
            except:
                return jsonify({"error": "Invalid token"}), 401

            if role and data["role"] != role:
                return jsonify({"error": "Forbidden"}), 403

            request.user = data
            return f(*args, **kwargs)
        return wrapper
    return decorator
