# CampusFind
**An AI-Powered Smart Lost-and-Found Management System for Educational Institutions**

CampusFind is a Flask web prototype for reporting lost and found belongings, searching reports, ranking possible matches with TF-IDF/cosine similarity, submitting private claims, and reviewing records as an administrator.

## Technology
- Frontend: HTML, CSS, Bootstrap 5, Jinja templates
- Backend: Python + Flask
- Database: SQLite
- Matching: scikit-learn TF-IDF + cosine similarity
- Tools: VS Code, Git, GitHub

## Features in this MVP
1. Register and log in (passwords are hashed).
2. Create lost or found reports with category, description, location, date and optional image.
3. Search and filter open reports.
4. View ranked possible matches from opposite report types in the same category.
5. Submit a private claim for review.
6. Admin can review claims and update item status.
7. Input validation and image file type/size restrictions.

**Important:** AI matching is decision support only. It does not prove ownership. A human/admin must verify a claim. Do not publish serial numbers, phone numbers, personal addresses, or unique identifying details in public descriptions.

## Run on Windows 11 (beginner steps)
1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ (tick **Add Python to PATH**).
2. Extract this project ZIP.
3. Open the extracted `CampusFind` folder in VS Code: **File → Open Folder**.
4. Open Terminal → New Terminal.
5. Create a virtual environment:
   ```powershell
   py -3.12 -m venv .venv
   ```
6. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run this once in the current terminal:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
7. Install packages:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
8. Start the website:
   ```powershell
   python app.py
   ```
9. Open http://127.0.0.1:5000 in Chrome or Edge. Keep the terminal open while using it.

The database `campusfind.db` is created automatically on first run.

## Administrator account
By default, the email `admin@campusfind.local` receives the admin role when registering. Register it yourself with a password you choose. For a different admin email, set `ADMIN_EMAIL` before running the app. Do not use the default development secret for a public deployment.

## Project structure
```text
CampusFind/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   ├── MIDWAY_PROGRESS.md
│   ├── TEST_CASES.md
│   ├── TEAM_CONTRIBUTIONS.md
│   └── GITHUB_GUIDE.md
├── tests/
│   └── test_matching.py
├── static/
│   ├── style.css
│   └── uploads/
└── templates/
```

## Current limitations / future work
- This is a local academic prototype, not a production campus service.
- No college SSO, email notifications, automated identity verification, or image-based AI matching.
- Admin moderation is basic; production use needs stronger access controls, CSRF protection, audit logs, backups, secure deployment and privacy review.
- Matching quality must be evaluated with a labeled dataset; do not claim accuracy until measured.

## Testing
Run the matching unit tests:
```powershell
python -m unittest discover -s tests -v
```
For full manual workflow test cases, see `docs/TEST_CASES.md`.
