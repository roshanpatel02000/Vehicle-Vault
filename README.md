[README.md](https://github.com/user-attachments/files/30583249/README.md)
# 🚗 Vehicle Vault - Django Application

Vehicle Vault is a full-featured Django web application for vehicle management, accessories, and notifications.

---

## 🛠️ Created Deployment Files

The following deployment configuration files have been added to the project for GitHub and Cloud hosting:

| File | Purpose |
| --- | --- |
| `.gitignore` | Prevents sensitive files (`.env`, `db.sqlite3`, `venv/`, `__pycache__`) from uploading to GitHub |
| `requirements.txt` | Defines all required Python dependencies (Django, Gunicorn, WhiteNoise, Psycopg2, etc.) |
| `Procfile` | Specifies the WSGI web process command for hosting servers |
| `build.sh` | Automated shell script to install dependencies, collect static files, and migrate database |
| `render.yaml` | 1-Click deployment blueprint for Render.com |
| `runtime.txt` | Specifies Python 3.11 version for production environment |
| `.env.example` | Template for environment variables |

---

## 🚀 How to Upload Project to GitHub

Run the following commands in your terminal inside the project root directory:

```bash
# 1. Initialize Git repository (if not already done)
git init

# 2. Add all files
git add .

# 3. Commit files
git commit -m "Add production deployment configurations for Vehicle Vault"

# 4. Rename main branch
git branch -M main

# 5. Add remote GitHub repository (Replace URL with your repository link)
git remote add origin https://github.com/YOUR_USERNAME/Vehicle-Vault.git

# 6. Push code to GitHub
git push -u origin main
```

---

## 🌐 FREE Places for Deployment

Here are the best **100% FREE hosting platforms** for Django & PostgreSQL:

### 1️⃣ **Render.com (Recommended - Best Overall Free Hosting)**
- **Free Plan**: Free Web Service + Free PostgreSQL database.
- **How to Deploy on Render**:
  1. Sign up at [Render.com](https://render.com).
  2. Click **New +** -> **Blueprint**.
  3. Connect your GitHub account and select your **Vehicle-Vault** repository.
  4. Render will automatically read `render.yaml` and provision both your Web Service & PostgreSQL Database for FREE!
  5. Click **Apply**. Your app will be live in 2-3 minutes.

---

### 2️⃣ **Koyeb (Fastest Free Micro Instances)**
- **Free Plan**: 1 Free Nano/Micro service with 512MB RAM.
- **How to Deploy on Koyeb**:
  1. Sign up at [Koyeb.com](https://koyeb.com).
  2. Connect your GitHub repository.
  3. Set Build command: `./build.sh`
  4. Set Start command: `gunicorn --chdir vehicle_vault vehicle_vault.wsgi:application`
  5. Add Environment Variables (`SECRET_KEY`, `DATABASE_URL`).

---

### 3️⃣ **PythonAnywhere (Simplest Python-Native Hosting)**
- **Free Plan**: 1 Free web app under `yourusername.pythonanywhere.com`.
- **How to Deploy**:
  1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com/).
  2. Clone your GitHub repository in the PythonAnywhere Bash console.
  3. Create a virtualenv, install `requirements.txt`, configure WSGI path to `vehicle_vault/vehicle_vault/wsgi.py`.

---

## 🗄️ Free PostgreSQL Databases

If you need a permanent free PostgreSQL database:
1. **[Neon.tech](https://neon.tech)** - Free 0.5 GB PostgreSQL cloud database (Never expires).
2. **[Supabase.com](https://supabase.com)** - 2 Free PostgreSQL projects (500 MB storage each).

Paste your database connection string into the `DATABASE_URL` environment variable.
