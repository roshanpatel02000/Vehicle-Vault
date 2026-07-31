<div align="center">

  <h1>🚘 Vehicle Vault</h1>
  <p><strong>A modern, full-stack Django platform for vehicle management, accessory shopping, comparison, and real-time notifications.</strong></p>

  [![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
  [![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Table of Contents
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Local Setup & Installation](#-local-setup--installation)
- [⚙️ Environment Variables](#️-environment-variables)
- [🌐 Free Deployment Guide](#-free-deployment-guide)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## ✨ Key Features

### 🏎️ Vehicle Exploration & Comparison
- Browse, search, and filter vehicles by make, model, category, and price range.
- Detailed vehicle specification pages with high-resolution image galleries.
- Side-by-side vehicle comparison tool.

### 🛠️ Accessories Store
- Browse compatible vehicle accessories and add-ons.
- Category filtering for performance parts, interior upgrades, and exterior modifications.

### 👤 User Management & Authentication
- Custom user profile system with role-based features.
- User dashboards to manage saved vehicles, inquiries, and orders.
- Secure email authentication & password recovery using Django SMTP.

### 🔔 Dynamic Notifications
- Real-time notification system for user updates, price drops, and system messages.
- Context-aware badge indicators in the main navigation bar.

### 🎨 Modern Responsive UI
- Built with custom responsive CSS, dynamic micro-interactions, and glassmorphism elements.

---

## 🛠️ Tech Stack

- **Backend Framework:** Django 6.0 / Python 3.11+
- **Database:** PostgreSQL (with SQLite support for local dev)
- **Production Web Server:** Gunicorn + WhiteNoise (Static asset handling)
- **Frontend:** HTML5, Modern Vanilla CSS, JavaScript, FontAwesome Icons
- **Email Service:** Django SMTP with Gmail App Password integration

---

## 📂 Project Structure

```text
VEHICLE_VAULT/
│
├── .env.example                # Template for environment variables
├── .gitignore                  # Git ignore rules for production security
├── build.sh                    # Render/Cloud deployment build script
├── Procfile                    # WSGI process file for Gunicorn
├── render.yaml                 # 1-Click deployment config for Render
├── requirements.txt            # Python dependencies list
├── runtime.txt                 # Production Python version definition
│
└── vehicle_vault/              # Main Django Application Root
    ├── manage.py               # Django CLI management script
    ├── static/                 # CSS, JavaScript, and static images
    ├── media/                  # User uploaded vehicle & accessory media
    ├── templates/              # HTML Templates (base, home, navbar, footer)
    │
    ├── core/                   # User authentication, profiles & dashboard
    ├── vehicle/                # Vehicle catalog, detail, search & comparison
    ├── accessory/              # Accessory store & product management
    ├── Notification/           # User notification system & context processor
    └── vehicle_vault/          # Project configuration (settings, urls, wsgi)
```

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.11+ installed on your system
- PostgreSQL installed and running (or use SQLite for dev)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Vehicle-Vault.git
cd Vehicle-Vault
```

### 2️⃣ Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-custom-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/vehicle_vault_db
```

### 5️⃣ Run Database Migrations
```bash
python vehicle_vault/manage.py makemigrations
python vehicle_vault/manage.py migrate
```

### 6️⃣ Create Superuser (Admin Access)
```bash
python vehicle_vault/manage.py createsuperuser
```

### 7️⃣ Run Development Server
```bash
python vehicle_vault/manage.py runserver
```
Visit `http://127.0.0.1:8000` in your web browser.

---

## 🌐 Free Deployment Guide

This project comes pre-configured for free deployment on **Render.com**, **Koyeb**, or **PythonAnywhere**.

### Deploying on Render.com (Recommended)
1. Push your repository to GitHub.
2. Sign up at [Render.com](https://render.com).
3. Click **New +** ➡️ **Blueprint**.
4. Select your **Vehicle-Vault** repository.
5. Render will automatically read `render.yaml` and provision your Web Service + PostgreSQL database for FREE!

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [Issues page](https://github.com/YOUR_USERNAME/Vehicle-Vault/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
