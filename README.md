# 🌱 HabitVerse

**HabitVerse** adalah aplikasi pelacak kebiasaan (habit tracker) modern berbasis **FastAPI** dengan antarmuka yang ringan, mobile-friendly, dan fun.  
Pengguna dapat membuat kebiasaan, melacak progres harian, melihat kalender heatmap, mendapatkan badge streak, serta menikmati **Quote of the Day** & **Daily Tip**.

---
Tampilan - Login
<img width="215" height="466" alt="Login - HabitVerse" src="https://github.com/user-attachments/assets/af686210-02cb-4cdb-bfd5-af4c8ebd34d4" />

Tampilan - Dashboard
<img width="215" height="888" alt="Dashboard • HabitVerse (1)" src="https://github.com/user-attachments/assets/75b00011-7065-4b2b-b6c3-ecf99efc8685" />

Tampilan - Habits
<img width="215" height="466" alt="Habits • HabitVerse" src="https://github.com/user-attachments/assets/14a64589-4f7c-4e14-bc14-129102052862" />

Tampilan - Community
<img width="215" height="541" alt="Community • HabitVerse" src="https://github.com/user-attachments/assets/6dbc1f60-95e1-40cc-bc2d-5f81dded9d25" />

Tampilan - AI Coach
<img width="215" height="540" alt="AI Coach • HabitVerse" src="https://github.com/user-attachments/assets/fa5e49c1-17cd-4e84-920c-afb0e98cfd75" />

---

## ✨ Fitur Utama
- ✅ Autentikasi & sesi pengguna
- ✅ CRUD Habits
- ✅ Progres harian + tombol **Complete** di dashboard
- ✅ Kalender Aktivitas (heatmap) 6 bulan terakhir
- ✅ Badge berdasarkan streak
- ✅ Quote of the Day & Daily Tips
- ✅ UI responsif (Tailwind, efek confetti 🎉)
- ✅ Dockerized (siap deploy)

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, Pydantic, SQLAlchemy, Alembic  
- **Database:** SQLite (default, `habitverse.db`)  
- **Frontend:** Tailwind (CDN), HTML server-rendered  
- **Auth:** Cookie-based  
- **Infra:** Docker, docker-compose, Nginx  

---

## 📂 Struktur Proyek
HabitVerse/
├── app/
│ ├── main.py # Entry FastAPI
│ ├── routes/ # Routes (dashboard, community, coach)
│ ├── api/ # REST API (habits, auth, dll.)
│ ├── core/ # Config DB & security
│ └── schemas/ # Pydantic models
├── infra/ # Dockerfile, docker-compose, nginx.conf
├── tests/ # Test API & fitur utama
├── requirements.txt
└── habitverse.db # DB default (ignored by git)

yaml
Salin
Edit

---

## 🚀 Menjalankan Secara Lokal

### 1) Setup Environment
```bash
git clone https://github.com/FaturRachmann/HabitVerse.git
cd HabitVerse

# Buat virtualenv
python -m venv venv

# Windows
venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
2) Jalankan Server (Development)
bash
python -m uvicorn app.main:app --reload --port 8001 --reload-dir app
👉 Akses: http://127.0.0.1:8001/dashboard

3) (Opsional) Migrasi Database
bash
alembic upgrade head
📌 Catatan:
File DB default: habitverse.db di root.
Endpoint login tersedia di app/api/auth.py (form sederhana/JSON).

📡 API Utama (Ringkas)
Habits
GET /api/habits/ → daftar habit
POST /api/habits/ → buat habit
GET /api/habits/{habit_id} → detail habit
DELETE /api/habits/{habit_id} → hapus habit
GET /api/habits/{habit_id}/logs?days=N → log N hari terakhir
POST /api/habits/{habit_id}/log → catat progres harian

json
{ "status": "completed", "count": 1 }
GET /api/habits/stats/heatmap?days=182 → data heatmap
Quote
GET /api/quotes/today → quote harian
🧪 Menjalankan Test
bash
pytest -q

🐳 Docker & Deployment
Build & run lokal (compose):
bash
cd infra
docker-compose up --build
Akses via nginx.conf (default port 80)
Konfigurasi ada di infra/Dockerfile & infra/nginx.conf
Sesuaikan env/secret (secret key, DB URL, dll.)

⚠️ Masalah Umum
Mobile tampilan zoomed → fix dengan viewport-fit=cover + responsive SVG heatmap
422 pada heatmap → gunakan endpoint /api/habits/stats/heatmap
Git CRLF/WSL → jangan commit venv/ dan file DB. Tambahkan ke .gitignore:
markdown
venv/
__pycache__/
*.pyc
habitverse.db
🗺️ Roadmap
🔔 Reminder / push notification
👥 Sharing progres komunitas
📥 Import/Export data
🌙 Dark mode
