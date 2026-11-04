import os, sqlite3, re
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "campusfind.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-development-secret")
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(_error):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_type TEXT NOT NULL CHECK(item_type IN ('lost','found')),
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        event_date TEXT NOT NULL,
        image_filename TEXT,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS claims(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TEXT NOT NULL,
        FOREIGN KEY(item_id) REFERENCES items(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    conn.close()

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Administrator access is required.", "danger")
            return redirect(url_for("dashboard"))
        return fn(*args, **kwargs)
    return wrapper

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def similarity_score(text_a, text_b):
    """Return cosine similarity from 0 to 1; zero if there is no usable text."""
    corpus = [text_a or "", text_b or ""]
    try:
        matrix = TfidfVectorizer(stop_words="english").fit_transform(corpus)
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        return 0.0

def find_matches(item, limit=5):
    opposite = "found" if item["item_type"] == "lost" else "lost"
    candidates = db().execute(
        "SELECT * FROM items WHERE item_type=? AND status='open' AND id<>? AND category=?",
        (opposite, item["id"], item["category"])
    ).fetchall()
    source = f'{item["title"]} {item["description"]} {item["location"]}'
    ranked = []
    for candidate in candidates:
        target = f'{candidate["title"]} {candidate["description"]} {candidate["location"]}'
        score = similarity_score(source, target)
        # Small metadata boost when the location text overlaps.
        if item["location"].lower() in candidate["location"].lower() or candidate["location"].lower() in item["location"].lower():
            score = min(1.0, score + 0.08)
        ranked.append((score, candidate))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return ranked[:limit]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 6:
            flash("Enter your name, a valid email, and a password of at least 6 characters.", "danger")
            return render_template("register.html")
        role = "admin" if email == os.environ.get("ADMIN_EMAIL", "admin@campusfind.local").lower() else "user"
        try:
            db().execute(
                "INSERT INTO users(name,email,password_hash,role,created_at) VALUES(?,?,?,?,?)",
                (name, email, generate_password_hash(password), role, datetime.now().isoformat(timespec="seconds"))
            )
            db().commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("That email is already registered.", "warning")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = db().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session.update(user_id=user["id"], name=user["name"], role=user["role"])
            return redirect(url_for("dashboard"))
        flash("Incorrect email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    items = db().execute("""
        SELECT items.*, users.name AS reporter FROM items
        JOIN users ON users.id=items.user_id
        ORDER BY items.created_at DESC LIMIT 30
    """).fetchall()
    my_items = db().execute("SELECT COUNT(*) AS n FROM items WHERE user_id=?", (session["user_id"],)).fetchone()["n"]
    return render_template("dashboard.html", items=items, my_items=my_items)

@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        item_type = request.form.get("item_type")
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        event_date = request.form.get("event_date", "")
        if item_type not in ("lost", "found") or not all([title, category, description, location, event_date]):
            flash("Please complete all required fields.", "danger")
            return render_template("report.html")
        image_filename = None
        image = request.files.get("image")
        if image and image.filename:
            if not allowed_file(image.filename):
                flash("Image must be PNG, JPG, JPEG, or WEBP.", "danger")
                return render_template("report.html")
            safe_name = secure_filename(image.filename)
            image_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{safe_name}'
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
        db().execute("""
            INSERT INTO items(user_id,item_type,title,category,description,location,event_date,image_filename,created_at)
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (session["user_id"], item_type, title, category, description, location, event_date,
              image_filename, datetime.now().isoformat(timespec="seconds")))
        db().commit()
        flash("Your report has been published.", "success")
        return redirect(url_for("dashboard"))
    return render_template("report.html")

@app.route("/search")
@login_required
def search():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    item_type = request.args.get("type", "").strip()
    sql = """SELECT items.*, users.name AS reporter FROM items
             JOIN users ON users.id=items.user_id WHERE items.status='open'"""
    params = []
    if q:
        sql += " AND (items.title LIKE ? OR items.description LIKE ? OR items.location LIKE ?)"
        params += [f"%{q}%"] * 3
    if category:
        sql += " AND items.category=?"
        params.append(category)
    if item_type in ("lost", "found"):
        sql += " AND items.item_type=?"
        params.append(item_type)
    sql += " ORDER BY items.created_at DESC"
    items = db().execute(sql, params).fetchall()
    return render_template("search.html", items=items, q=q, category=category, item_type=item_type)

@app.route("/item/<int:item_id>")
@login_required
def item_detail(item_id):
    item = db().execute("""SELECT items.*, users.name AS reporter FROM items
                           JOIN users ON users.id=items.user_id WHERE items.id=?""", (item_id,)).fetchone()
    if not item:
        flash("Report not found.", "warning")
        return redirect(url_for("dashboard"))
    matches = find_matches(item)
    return render_template("item.html", item=item, matches=matches)

@app.route("/claim/<int:item_id>", methods=["POST"])
@login_required
def claim(item_id):
    item = db().execute("SELECT * FROM items WHERE id=? AND status='open'", (item_id,)).fetchone()
    message = request.form.get("message", "").strip()
    if not item or item["user_id"] == session["user_id"] or len(message) < 10:
        flash("Claim could not be submitted. Add at least 10 characters of private identifying proof.", "danger")
        return redirect(url_for("item_detail", item_id=item_id))
    db().execute("INSERT INTO claims(item_id,user_id,message,created_at) VALUES(?,?,?,?)",
                 (item_id, session["user_id"], message, datetime.now().isoformat(timespec="seconds")))
    db().commit()
    flash("Claim submitted for review. Do not share sensitive details publicly.", "success")
    return redirect(url_for("item_detail", item_id=item_id))

@app.route("/admin")
@admin_required
def admin():
    items = db().execute("""SELECT items.*, users.name AS reporter FROM items
                            JOIN users ON users.id=items.user_id ORDER BY items.created_at DESC""").fetchall()
    claims = db().execute("""SELECT claims.*, items.title, users.name AS claimant FROM claims
                             JOIN items ON items.id=claims.item_id
                             JOIN users ON users.id=claims.user_id ORDER BY claims.created_at DESC""").fetchall()
    return render_template("admin.html", items=items, claims=claims)

@app.route("/admin/item/<int:item_id>", methods=["POST"])
@admin_required
def admin_update_item(item_id):
    status = request.form.get("status")
    if status not in ("open", "returned", "resolved"):
        flash("Invalid status.", "danger")
    else:
        db().execute("UPDATE items SET status=? WHERE id=?", (status, item_id))
        db().commit()
        flash("Item status updated.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/claim/<int:claim_id>", methods=["POST"])
@admin_required
def admin_update_claim(claim_id):
    status = request.form.get("status")
    if status in ("approved", "rejected", "pending"):
        db().execute("UPDATE claims SET status=? WHERE id=?", (status, claim_id))
        db().commit()
        flash("Claim reviewed.", "success")
    return redirect(url_for("admin"))

@app.errorhandler(413)
def too_large(_error):
    flash("Image is too large. Maximum upload size is 4 MB.", "danger")
    return redirect(url_for("report"))

@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
