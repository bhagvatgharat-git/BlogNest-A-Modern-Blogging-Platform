# BlogNest – A Modern Blogging Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-0284c7.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20WAL-003B57.svg)](https://www.sqlite.org/)
[![Design](https://img.shields.io/badge/Theme-Light%20Blue%20%26%20White-0ea5e9.svg)](/)
[![Tests](https://img.shields.io/badge/Tests-16%20Passing-10b981.svg)](/)

A full-stack, internship-grade blogging web application built using **Python Flask**, **SQLite**, **Flask-SQLAlchemy**, and a custom **Light Blue & White** modern UI design system.

---

## 🌟 Project Specifications & Highlights

| Feature / Item | Implementation Specification |
|---|---|
| **Project Name** | **BlogNest** |
| **Project Type** | Full-Stack Web Application |
| **Backend Framework** | Python Flask (Application Factory & Blueprints) |
| **Database & ORM** | SQLite + Flask-SQLAlchemy |
| **Authentication** | Flask-Login with Session Management |
| **Password Security** | Werkzeug PBKDF2:SHA256 password hashing |
| **Frontend UI** | HTML5, CSS3 (Light Blue & White Design System), Vanilla JS |
| **Production WSGI** | Waitress / Gunicorn compatible |
| **Test Coverage** | 16 Automated Unit & Integration Tests (100% pass) |

---

## 🎯 10 Core User Capabilities

1. **Secure Registration & Login**: Validated user signup, duplicate prevention, and remember-me session persistence.
2. **Create & Publish Blog Posts**: Rich editor form with title, cover image URL, category selection, summary, and formatted markdown body.
3. **Private Drafts**: Save unfinished stories as drafts. **Drafts are strictly isolated and visible only to their author**.
4. **Edit & Delete Authorization**: Users can only update or remove their own posts; unauthorized attempts return `403 Forbidden`.
5. **Community Blog Browsing**: Clean paginated homepage feed, featured story card, and category ribbons.
6. **Discussion & Commenting**: Authenticated readers can share feedback; both the comment author and post author can moderate/delete comments.
7. **Multi-field Search**: Search published stories in real-time by title, summary, or content keyword.
8. **Topic & Category Filtering**: Filter posts by technology, design, artificial intelligence, architecture, and lifestyle.
9. **Author Dashboard & Statistics**: Personal author dashboard showing total published articles, drafts, total views, and community comments.
10. **Author Profiles & Reading Time**: Calculated estimated reading times for every article and public author portfolio pages.

---

## 🏗️ Architecture & Directory Structure

```text
BlogNest – A Modern Blogging Platform/
│
├── app/
│   ├── __init__.py            # Flask application factory, Jinja filters, context processors
│   ├── models.py              # User, Category, Post, and Comment SQLAlchemy models
│   ├── routes/
│   │   ├── __init__.py        # Blueprint packages
│   │   ├── auth.py            # Authentication routes (login, register, logout, profile)
│   │   ├── blog.py            # Post CRUD, draft privacy, and comment moderation
│   │   ├── dashboard.py       # Author analytics, posts management, drafts tabs
│   │   └── main.py            # Homepage, explore/search, author public portfolios
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css       # Custom Light Blue & White Design System
│   │   └── js/
│   │       └── main.js        # Mobile toggle, copy-link share, alert dismissals
│   └── templates/
│       ├── base.html          # HTML5 layout shell, navbar, alerts, footer
│       ├── auth/              # login.html, register.html, profile.html
│       ├── blog/              # post_detail.html, create_post.html, edit_post.html
│       ├── components/        # navbar.html, footer.html, blog_card.html, pagination.html
│       ├── dashboard/         # index.html (analytics metrics, published posts, drafts)
│       ├── errors/            # 404.html, 500.html
│       └── main/              # index.html, explore.html, author.html, about.html
│
├── instance/
│   └── blognest.db            # SQLite persistent database file
├── tests/
│   ├── test_auth.py           # Authentication & password hashing tests
│   ├── test_blog_crud.py      # Post creation, editing, deleting, and draft privacy tests
│   ├── test_comments.py       # Comment addition, listing, author stats, and moderation tests
│   └── test_search.py         # Search keywords, category filter, and sorting tests
│
├── config.py                  # Base, development, and test configurations
├── requirements.txt           # Python dependencies (Flask, SQLAlchemy, Login, Waitress)
├── run.py                     # Development server entry point
├── seed_data.py               # Database seeder script with sample authors & articles
└── README.md                  # Comprehensive project documentation
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone
git clone https://github.com/bhagvatgharat-git/BlogNest-A-Modern-Blogging-Platform.git
cd BlogNest-A-Modern-Blogging-Platform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed Realistic Sample Data
Populate the database with sample authors, categories, rich articles, and comments:
```bash
python seed_data.py
```
> **Sample Login Credentials**:
> - **Lead Author**: `username`: `bhagvat` | `password`: `Admin123!`
> - **UI Designer**: `username`: `sarah_ux` | `password`: `Designer123!`
> - **Cloud Engineer**: `username`: `alex_cloud` | `password`: `Cloud123!`

### 5. Launch the Development Server
```bash
python run.py
```
Open your browser at `http://127.0.0.1:5000`.

---

## 🧪 Running Automated Tests

Run the full automated test suite covering all 10 project requirements:
```bash
python -m unittest discover tests -v
```
**Test Results**: `16 passed, 0 failed` across:
- `test_auth.py`
- `test_blog_crud.py`
- `test_comments.py`
- `test_search.py`

---

## 🚢 Production Deployment

For production deployments, use the included WSGI production server (`waitress` or `gunicorn`):

### Using Waitress (Windows & Linux Cross-Platform):
```bash
waitress-serve --port=5000 run:app
```

### Environment Configuration:
Create a `.env` file from `.env.example`:
```env
FLASK_ENV=production
SECRET_KEY=generate-a-strong-random-key-here
DATABASE_URL=sqlite:///instance/blognest.db
```

---

## 📋 Internship Task Completion Checklist

- [x] **Task 1: Prepare Yourself – Installation & Setup**
  - Python virtual environment, VS Code setup, Git repository initialized.
- [x] **Task 2: Flask Setup and Basic Structure**
  - Application factory, blueprints architecture, SQLite database and models.
- [x] **Task 3: User Authentication**
  - Registration, password hashing, session management, route protection.
- [x] **Task 4: Blog Post CRUD Functionality**
  - Post creation, editing, deletion, slug generation, and draft state isolation.
- [x] **Task 5: Frontend: Posts and Navigation**
  - Light Blue & White design system, cards, dashboard metrics, responsive navbar.
- [x] **Task 6: Commenting System**
  - Article discussion threads, author badges, comment moderation rights.
- [x] **Task 7: Search and Filtering**
  - Explore page with keyword search, category filters, and views/date sorting.
- [x] **Task 8: Deployment Preparation and Testing**
  - 16 passing unit/integration tests, production WSGI configuration, sample database seeder.
- [x] **Task 9: Demonstration Walkthrough & Video Guide**
  - Documented verification steps and demonstration script.

---

## 🎥 Task 9: Demonstration Video Walkthrough Script

When recording your internship completion video, follow this quick 3-minute sequence:
1. **Homepage & Theme Showcase**: Show the clean Light Blue & White hero section, community stats ribbon, and category filters.
2. **User Authentication**: Log in as `bhagvat` (or register a new user). Show the customized avatar and profile pill in the navbar.
3. **Write a Story**: Click "✍️ Write", fill in title, select category, upload cover image, and save first as "Save as Draft".
4. **Author Dashboard & Draft Privacy**: Show the dashboard with stats, click "Drafts" tab. Open an incognito window to prove the draft link returns `404 Not Found` for unauthenticated visitors.
5. **Publish & Reading Time**: Edit the draft and hit "Publish Story". Show the estimated reading time calculation (e.g. `2 min read`).
6. **Commenting System**: Open another user's post, post a thoughtful comment in the discussion section. Show the author badge and delete button.
7. **Search & Filter**: Go to "Explore", type a keyword (e.g., `Flask`), and filter by category (e.g., `Web Development`). Show sorting by `Most Viewed`.
8. **Run Test Suite in Terminal**: Run `python -m unittest discover tests` to show all 16 tests passing cleanly.

---

*Crafted with precision by Bhagvat Gharat for the Web Development Internship.*
