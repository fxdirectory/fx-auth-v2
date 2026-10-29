# Auth Microservice (Flask + MySQL)

API auth microservice sederhana menggunakan Flask. Login cukup dengan **username & password**, token disimpan di kolom `token` pada tabel `users`.

## Struktur Project

```
.
├── conf/                  # Konfigurasi (config.py, baca dari .env)
├── db/
│   ├── migrations/        # SQL create table
│   ├── seeds/             # SQL data awal
│   └── run_db.py          # Jalankan migration + seeder dari Python
├── function/              # Function controller (logika user: login, register, dll)
├── middle/                # Middleware (token_required, role_required)
├── routes/                # Blueprint routes (auth_routes.py, user_routes.py)
├── utils/                 # Helper (koneksi db, response JSON)
├── venv/                  # Virtual environment
├── main.py                # Entry point aplikasi
├── requirements.txt
└── .env                   # Kredensial MySQL & konfigurasi app
```

## Kolom Tabel `users`

| Kolon      | Tipe         | Keterangan                              |
|------------|--------------|-----------------------------------------|
| id         | INT AI PK    |                                         |
| username   | VARCHAR(100) | unik                                    |
| password   | VARCHAR(255) | hash (werkzeug pbkdf2), bukan plain text|
| token      | VARCHAR(64)  | token login aktif (NULL jika logout)    |
| role       | VARCHAR(50)  | `admin` / `user`                        |
| last_login | DATETIME     | di-update saat login berhasil           |
| created_at | DATETIME     | auto                                    |

## Cara Menjalankan

1. **Siapkan MySQL**, lalu sesuaikan `.env` (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME).

2. **Install dependensi** (venv sudah tersedia, atau buat ulang):
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Jalankan migration & seeder** (otomatis membuat database + tabel + user awal):
   ```bash
   python db/run_db.py
   ```
   Atau manual dengan client mysql:
   ```bash
   mysql -u root -p < db/migrations/001_create_users_table.sql
   ```

4. **Jalankan aplikasi**:
   ```bash
   python main.py
   ```

User hasil seeder: `admin / admin123` (role admin), `user1 / password123` (role user).

## Endpoint

| Method | URL                 | Header Authorization | Deskripsi                    |
|--------|---------------------|----------------------|------------------------------|
| POST   | /api/auth/login     | -                    | Login (username + password)  |
| POST   | /api/auth/logout    | wajib               | Logout (token di-NULL-kan)   |
| POST   | /api/users/register | -                    | Daftar user baru             |
| GET    | /api/users/me       | wajib               | Profil user yang login       |
| GET    | /api/users/         | wajib (admin)        | Daftar semua user            |

### Contoh

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
Respons:
```json
{
  "success": true,
  "message": "Login berhasil",
  "data": {
    "token": "a1b2c3...",
    "user": {"id": 1, "username": "admin", "role": "admin", "last_login": "...", "created_at": "..."}
  }
}
```

**Akses endpoint yang dilindungi (pakai token dari login):**
```bash
curl http://localhost:5000/api/users/me -H "Authorization: <token>"
```

**Logout:**
```bash
curl -X POST http://localhost:5000/api/auth/logout -H "Authorization: <token>"
```

**Register:**
```bash
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"budi","password":"rahasia123"}'
```
