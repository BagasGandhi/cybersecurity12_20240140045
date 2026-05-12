





import os
import sqlite3
from flask import Flask, redirect, request, session, render_template_string
from jinja2 import Template


app = Flask(__name__)
app.secret_key = 'sqlinjection'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# ===== EMBEDDED CSS =====
EMBEDDED_CSS = """
:root {
  --primary: #6366f1;
  --secondary: #8b5cf6;
  --accent: #06b6d4;
  --danger: #ef4444;
  --surface: rgba(255, 255, 255, 0.92);
  --text: #1f2937;
  --muted: #6b7280;
  --border: rgba(255, 255, 255, 0.35);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  min-height: 100vh;
  font-family: Inter, 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background:
    radial-gradient(circle at top left, rgba(255,255,255,.35), transparent 28%),
    linear-gradient(135deg, #6366f1 0%, #8b5cf6 48%, #06b6d4 100%);
  color: var(--text);
  overflow-x: hidden;
}

body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: radial-gradient(rgba(255,255,255,.22) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
}

.custom-navbar {
  background: rgba(17, 24, 39, 0.22);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow: 0 10px 30px rgba(17, 24, 39, 0.12);
  padding: 1rem 0;
}

.navbar-brand {
  font-weight: 800;
  letter-spacing: -0.03em;
  font-size: 1.35rem;
}

.navbar-text {
  background: rgba(255,255,255,.16);
  border: 1px solid rgba(255,255,255,.22);
  border-radius: 999px;
  padding: .45rem .85rem;
}

.logout-btn {
  border-radius: 999px;
  padding: .45rem .9rem !important;
  background: rgba(255,255,255,.14);
  transition: .25s ease;
}

.logout-btn:hover {
  background: rgba(255,255,255,.25);
  transform: translateY(-2px);
}

.container {
  position: relative;
  z-index: 1;
}

.page-title {
  font-size: clamp(2rem, 5vw, 3.4rem);
  font-weight: 900;
  letter-spacing: -0.06em;
  color: #fff;
  text-shadow: 0 10px 28px rgba(17, 24, 39, 0.18);
}

.subtitle {
  color: rgba(255,255,255,.84) !important;
  font-size: 1.05rem;
}

.glass-effect {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  backdrop-filter: blur(18px);
  box-shadow: 0 24px 70px rgba(17, 24, 39, 0.16);
  overflow: hidden;
  animation: slideUp .55s ease both;
}

.glass-effect:hover {
  transform: translateY(-4px);
  box-shadow: 0 30px 80px rgba(17, 24, 39, 0.2);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

.card-title,
.section-title {
  font-weight: 800;
  letter-spacing: -0.02em;
}

.entry-card .card-title,
.search-card .card-title {
  color: var(--primary);
}

.section-title {
  color: #fff;
  text-shadow: 0 8px 24px rgba(17, 24, 39, .16);
}

.entry-input,
.search-input,
.login-form input {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 14px 16px;
  font-size: 1rem;
  background: #f9fafb;
  transition: .22s ease;
}

.entry-input:focus,
.search-input:focus,
.login-form input:focus {
  background: #fff;
  border-color: var(--primary);
  box-shadow: 0 0 0 .22rem rgba(99, 102, 241, .16);
  outline: none;
}

.btn-post,
.search-group .btn-primary,
.login-form button {
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #fff;
  font-weight: 800;
  padding: 13px 22px;
  transition: .22s ease;
  box-shadow: 0 12px 24px rgba(99, 102, 241, .25);
}

.btn-post:hover,
.search-group .btn-primary:hover,
.login-form button:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 32px rgba(99, 102, 241, .34);
}

.timeline-item {
  margin-bottom: 18px;
  border-left: 6px solid var(--accent);
}

.timeline-content {
  font-size: 1.05rem;
  color: var(--text);
  line-height: 1.7;
  word-break: break-word;
}

.quote-icon {
  color: var(--primary);
  opacity: .55;
}

.btn-delete {
  width: 38px;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #fee2e2;
  color: var(--danger);
  border: none;
  border-radius: 14px;
  transition: .22s ease;
}

.btn-delete:hover {
  background: var(--danger);
  color: #fff;
  transform: translateY(-2px);
}

.search-group {
  gap: 8px;
}

.search-group .search-input,
.search-group .btn-primary {
  border-radius: 16px !important;
}

.stat-icon {
  width: 72px;
  height: 72px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 24px;
  color: #fff;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  font-size: 2rem;
  box-shadow: 0 16px 34px rgba(6, 182, 212, .28);
}

.alert {
  border: 1px dashed rgba(99, 102, 241, .45);
  border-radius: 20px;
  background: rgba(255,255,255,.78);
  color: var(--primary);
  font-weight: 700;
  padding: 22px;
}

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-box {
  width: 100%;
  max-width: 420px;
  padding: 42px 34px;
  border-radius: 28px;
  background: rgba(255,255,255,.94);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255,255,255,.4);
  box-shadow: 0 30px 90px rgba(17, 24, 39, .24);
  animation: slideUp .55s ease both;
}

.login-title {
  text-align: center;
  color: var(--primary);
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: -0.05em;
}

.login-subtitle {
  text-align: center;
  color: var(--muted);
  margin: 8px 0 32px;
}

.login-form button {
  width: 100%;
  margin-top: 4px;
}

@media (max-width: 768px) {
  .navbar-collapse {
    display: block !important;
  }

  .navbar-nav {
    flex-direction: row;
    align-items: center;
    gap: 10px;
    margin-top: 12px;
  }

  .entry-card form {
    flex-direction: column;
  }

  .btn-post {
    width: 100%;
  }
}
"""

# ===== EMBEDDED HTML TEMPLATE =====
TIMELINE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Timeline App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
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
                <p class="subtitle text-muted">Bagikan pikiran dan momen terbaikmu</p>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-lg-8">
                <div class="card glass-effect entry-card">
                    <div class="card-body p-4">
                        <h5 class="card-title mb-3">
                            <i class="fas fa-feather me-2"></i>Buat Postingan Baru
                        </h5>
                        <form action="/create" method="post" class="d-flex gap-2">
                            <input name="content" class="form-control entry-input" 
                                   placeholder="Tulis sesuatu..." required>
                            <button type="submit" class="btn btn-primary btn-post">
                                <i class="fas fa-paper-plane me-1"></i>Post
                            </button>
                        </form>
                    </div>
                </div>

                <div class="timeline-container mt-4">
                    <h5 class="section-title mb-4">
                        <i class="fas fa-clock me-2"></i>Postingan Terbaru
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
                        <i class="fas fa-inbox me-2"></i>Belum ada postingan. Mulai tulis sesuatu!
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="col-lg-4">
                <div class="card glass-effect search-card">
                    <div class="card-body p-4">
                        <h5 class="card-title mb-3">
                            <i class="fas fa-search me-2"></i>Cari Postingan
                        </h5>
                        <form action="/search" method="get">
                            <div class="input-group search-group">
                                <input name="keyword" class="form-control search-input" 
                                       placeholder="Cari isi postingan..." autocomplete="off">
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
                        <h6 class="card-title">Selamat Datang!</h6>
                        <p class="text-muted small">Terus bagikan momen terbaikmu</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

LOGIN_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login - Timeline App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{ css }}</style>
</head>
<body>
    <div class="login-container">
        <div class="login-box">
            <div class="login-title">
                <i class="fas fa-timeline me-2"></i>TimelineApp
            </div>
            <p class="login-subtitle">Masuk untuk melanjutkan</p>
            <form method="post" class="login-form">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">
                    <i class="fas fa-sign-in-alt me-2"></i>Login
                </button>
            </form>
            <p style="text-align: center; margin-top: 20px; color: #999; font-size: 0.9rem;">
                <i class="fas fa-info-circle me-1"></i>Demo: alice/alicepw atau bob/bobpw
            </p>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
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
    query = "SELECT id, user_id, content FROM time_line WHERE content LIKE ?"
    cur.execute(query, ('%' + keyword + '%',))
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
