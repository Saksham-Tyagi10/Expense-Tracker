# Expense-Tracker

A lightweight, secure, and responsive full-stack web application designed to track personal finances, manage daily income and expenses, and visualize spending habits through interactive analytics. Built with Python (Flask), SQLite, Bootstrap 5, and Chart.js.

---

## 🌟 Key Features

* **Multi-User Authentication**: Secure user registration and login with session management and password hashing using Werkzeug.
* **Per-User Isolation**: Each registered user gets an isolated financial workspace; data is strictly partitioned and private.
* **Complete CRUD Operations**: Add, view, categorize, and delete income/expense transactions with live balance updates.
* **Visual Analytics**: Interactive doughnut charts powered by **Chart.js** displaying dynamic category-wise expense breakdowns.
* **Payment Method Tagging**: Track whether payments were made via UPI, Cash, Card, or Net Banking.
* **Responsive UI**: Clean, mobile-friendly interface built with modern Bootstrap 5 components.

---

## 🛠️ Tech Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5 |
| **Data Visualization** | Chart.js |
| **Backend** | Python 3, Flask (RESTful Endpoints, Session Auth) |
| **Database** | SQLite3 |
| **Security** | Werkzeug (`generate_password_hash`, `check_password_hash`) |
| **WSGI / Deployment** | Gunicorn, Render |

---

## 🗄️ Database Architecture

The relational schema ensures data integrity through foreign keys:

* **`users`**: Manages credentials (`user_id`, `username`, `email`, `password_hash`, `created_at`).
* **`categories`**: Stores transaction types (`category_id`, `category_name`, `icon_url`).
* **`transactions`**: Stores financial records (`transaction_id`, `user_id`, `category_id`, `type`, `amount`, `date`, `description`, `payment_method`).

---

## 📂 Project Structure

```text
expense-tracker/
│
├── app.py                # Main Flask application and API route controllers
├── database.py           # SQLite connection & schema initialization
├── requirements.txt      # Python dependencies (Flask, Gunicorn)
├── Procfile              # Deployment command for web servers
├── .gitignore            # Ignored files (database, cache)
│
├── templates/
│   ├── index.html        # Main dashboard UI
│   └── login.html        # Authentication page (Login/Register)
│
└── static/
    └── app.js            # Client-side logic, API calls, and chart updates
