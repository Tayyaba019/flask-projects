💰 Expense Tracker — Smart Finance Made Simple

Expense Tracker is a modern, full-featured Flask web application designed to help users manage, visualize, and control their spending with ease.
It provides secure authentication, data filtering, chart visualization, and CSV export — all wrapped in a beautiful TailwindCSS-powered interface.

🚀 Features
🔐 User Authentication

Secure Signup, Login, and Logout functionality.

Passwords are safely hashed before storage.

Each user has their own expense dashboard and private data.

💵 Expense Management

Add, view, and delete your daily expenses.

Filter expenses by date range or category.

See detailed insights with dynamic charts and totals.

📊 Data Visualization

Interactive Pie Chart showing category-wise expense breakdown.

Bar Chart displaying daily expense totals.

Charts generated using Matplotlib and displayed dynamically.

📦 Export & Backup

Download your filtered data as a CSV file for personal records.

🎨 Responsive Design

Built with TailwindCSS for a modern, mobile-friendly layout.

Separate layouts for:

Authentication pages (Login, Signup)

Dashboard and expense management pages

🧠 Tech Stack
Category	Technology
Frontend	HTML5, TailwindCSS, Jinja2 Templates
Backend	Flask (Python)
Database	SQLite (via SQLAlchemy ORM)
Authentication	Flask-Login, Werkzeug Security
Data Visualization	Matplotlib
Deployment (optional)	PythonAnywhere / Render / Vercel

🏗️ Project Structure
Expense_Tracker_App/
│
├── app.py                  # Main Flask application
├── models.py               # Database models (User, Expense)
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Dashboard layout
│   ├── base_auth.html      # Auth page layout
│   ├── home.html           # Landing page
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
│   ├── dashboard.html      # Main dashboard
│   ├── add.html            # Add expense form
│   ├── view.html           # View expenses page
│   └── index.html          # Filter & chart page
│
├── static/                 # CSS / JS / images (if any)
├── instance/               # SQLite database file (.db)
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation

⚙️ Setup & Installation

1️⃣ Clone the Repository


2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Initialize the Database

Open a Python shell inside your project folder:

python
>>> from app import db
>>> db.create_all()
>>> exit()

5️⃣ Run the Application
flask run


Then open the app in your browser:

http://127.0.0.1:5000/

📜 License

This project is licensed under the MIT License — you’re free to use, modify, and distribute it with attribution.