"""Route user: register, profil (perlu token), daftar user khusus admin."""
from flask import Blueprint, request, g

from function.user_function import create_user, get_user_by_username, public_user
from middle.auth_middleware import token_required, role_required
from utils.db import query
from utils.response import success, error

user_bp = Blueprint("user", __name__, url_prefix="/api/users")


@user_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return error("Username dan password wajib diisi.", 400)
    if len(password) < 6:
        return error("Password minimal 6 karakter.", 400)
    if get_user_by_username(username):
        return error("Username sudah dipakai.", 409)

    new_id = create_user(username, password)
    if new_id is None:
        return error("Gagal mendaftar.", 500)

    user = query("SELECT * FROM users WHERE id = %s", (new_id,), fetch_one=True)
    return success("Registrasi berhasil", public_user(user), 201)


@user_bp.get("/me")
@token_required
def me():
    """Ambil data user yang sedang login."""
    return success("OK", public_user(g.current_user))


@user_bp.get("/")
@token_required
@role_required("admin")
def list_users():
    """Hanya admin: tampilkan semua user."""
    rows = query("SELECT * FROM users ORDER BY id", fetch_all=True)
    return success("OK", [public_user(u) for u in rows])
