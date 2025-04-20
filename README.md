# 🎁 GiftEase

A simple and user-friendly web platform where users can **buy** and **sell** unused gift cards with ease and security.

---

## 📋 Table of Contents

1. [💡 Project Overview](#-project-overview)
2. [🚀 Features](#-features)
3. [🛠 Tech Stack](#-tech-stack)
4. [📦 Installation & Setup](#-installation-steps)

---

## 💡 Project Overview

This platform enables users to:
- List unused gift cards for sale.
- Browse available gift cards and purchase at discounted prices.
- Receive payment securely upon successful sale.

No need for buyer/seller profiles—**any user can both buy and sell**!

---

## 🚀 Features

- 🛒 Buy gift cards at discounted rates
- 💳 Sell unused gift cards securely
- 🔍 Search & filter cards by brand, value, expiry
- 📩 Email confirmation on transactions
- 🔐 CSRF protection and validation
- 📁 Easy-to-use dashboard
- 🎨 Responsive design with Bootstrap

---

## 🛠 Tech Stack

| Layer         | Tech Used                 |
| ------------- | ------------------------- |
| Frontend      | HTML, CSS, Bootstrap, Django Templates |
| Backend       | Django (Python)           |
| Database      | SQLite (default) / PostgreSQL (optional) |
| Miscellaneous | Miro for diagrams, Git for version control |

---

## 📦 Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Brahmiboyalla/GiftEase.git
cd giftcard-platform

# 2. Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (for admin access)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

---

## User Guide

### Create an account with valid email address for smooth experience
### Create an email account for the platform and update the settings file at `core/settings.py`
