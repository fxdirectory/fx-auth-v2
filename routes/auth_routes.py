from flask import Blueprint, request, g
from function.user_function import login_user, logout_user, public_user
from middle.auth_middleware import token_required
from utils.response import success, error

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return error("Username dan password wajib diisi.", 400)
    user = login_user(username, password)
    if not user:
        return error("Username atau password salah.", 401)
    return success("Login berhasil", {"token": user["token"], "user": public_user(user)})

@auth_bp.post("/logout")
@token_required
def logout():
    logout_user(g.current_user["id"])
    return success("Logout berhasil")
