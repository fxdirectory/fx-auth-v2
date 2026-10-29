"""Middleware autentikasi berbasis token (header Authorization)."""
from functools import wraps

from flask import request, g

from function.user_function import get_user_by_token  # noqa: F401 (dipakai juga oleh routes)
from utils.response import error


def token_required(f):
    """
    Decorator: wajib menyertakan header:
        Authorization: <token>
    Token dicocokkan dengan kolom `token` pada tabel users.
    User yang cocok disimpan di `g.current_user`.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").strip()
        if not token:
            return error("Token tidak ditemukan. Gunakan header Authorization.", 401)

        user = get_user_by_token(token)
        if not user:
            return error("Token tidak valid atau sudah logout.", 401)

        g.current_user = user
        return f(*args, **kwargs)

    return decorated


def role_required(role):
    """Decorator: hanya user dengan role tertentu yang boleh akses."""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(__import__("flask").g, "current_user", None)
            if user is None:
                return error("Harus login dulu.", 401)
            if user["role"] != role:
                return error("Akses ditolak. Harus berperan sebagai %s." % role, 403)
            return f(*args, **kwargs)

        return decorated

    return decorator
