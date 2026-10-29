import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from werkzeug.security import generate_password_hash  # noqa: E402
from utils.db import get_connection  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
MIGRATION_DIR = os.path.join(BASE, "migrations")
SEED_SQL = os.path.join(BASE, "seeds", "001_seed_users.sql")


def run_sql_file(conn, path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    with conn.cursor() as cur:
        for stmt in [s.strip() for s in sql.split(";") if s.strip() and not s.strip().startswith("--")]:
            # buang baris komentar di awal statement
            lines = [ln for ln in stmt.splitlines() if not ln.strip().startswith("--")]
            stmt = "\n".join(lines).strip()
            if stmt:
                cur.execute(stmt)
    conn.commit()
    print(f"[OK] {os.path.relpath(path, BASE)}")


def seed_users():
    conn = get_connection()
    users = [
        ("admin", generate_password_hash("admin123"), "admin"),
        ("user1", generate_password_hash("password123"), "user"),
    ]
    with conn.cursor() as cur:
        for username, pw_hash, role in users:
            cur.execute(
                """INSERT INTO users (username, password, role)
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE password = VALUES(password), role = VALUES(role)""",
                (username, pw_hash, role),
            )
    conn.commit()
    conn.close()
    print("[OK] Seeder user selesai:")
    print("     - admin / admin123   (role: admin)")
    print("     - user1 / password123 (role: user)")


if __name__ == "__main__":
    # 1. Migration (koneksi tanpa database dulu agar CREATE DATABASE berhasil)
    conn = get_connection(database=None)
    for fn in sorted(os.listdir(MIGRATION_DIR)):
        if fn.endswith(".sql"):
            run_sql_file(conn, os.path.join(MIGRATION_DIR, fn))
    conn.close()
    seed_users()
    print("Selesai.")
