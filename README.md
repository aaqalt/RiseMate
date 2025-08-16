# 🌅 RISEMATE Telegram Bot

RISEMATE is a personal productivity assistant Telegram bot that sends you a **good morning message every day** with:  
- 🌤️ **Weather update** (from API)  
- 💡 **Inspirational quote** (from famous people)  
- ✅ **Your personal to-do list** (saved in the bot)  

Built with **Python**, **Aiogram**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **APScheduler**.  

---

## ✨ Features
- 📩 Daily scheduled **morning messages** with weather, quotes, and tasks.  
- ✅ Manage your **to-do list** (add, view, remove tasks).  
- 🌤️ Fetches real-time **weather updates** via external API.  
- 💬 Motivational **quotes from famous people**.  
- 🗄️ Persistent storage with **PostgreSQL** (via SQLAlchemy + Alembic migrations).  
- ⏰ **APScheduler** for sending messages on schedule.  

---

## 🛠️ Tech Stack
- [Python 3.12+](https://www.python.org/)  
- [Aiogram](https://docs.aiogram.dev/en/latest/) – Telegram bot framework  
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for PostgreSQL  
- [Alembic](https://alembic.sqlalchemy.org/) – database migrations  
- [APScheduler](https://apscheduler.readthedocs.io/) – scheduling tasks  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/aaqalt/risemate.git
cd risemate
