# CampusFind – Project Documentation

## 1. Abstract
CampusFind is a web-based lost-and-found management prototype for educational institutions. It centralizes item reports and uses text similarity to rank possible lost/found matches. Users can submit reports, search open records and send private claim evidence. An administrator can review claims and update item status.

## 2. Problem statement
Campus lost-property information may be spread across messaging groups, notice boards and word of mouth. Descriptions can vary, making manual matching difficult. Users may also lack a clear way to track whether an item has been found, claimed or returned.

## 3. Objectives
- Centralize lost and found reporting.
- Search and filter reports by text, category and report type.
- Rank possible matches using TF-IDF and cosine similarity.
- Support private claim submission and status updates.
- Provide a basic administrator review page.

## 4. Scope
The current MVP is a local web prototype using sample or voluntarily collected reports. Text-based matching is included. Image similarity, email notifications and college login integration are future extensions. The system does not automatically verify identity or guarantee that two reports describe the same object.

## 5. System requirements
**Software:** Python 3.11/3.12, Flask, scikit-learn, SQLite, HTML/CSS/Bootstrap, VS Code, browser, Git/GitHub.

**Hardware:** A standard laptop/desktop capable of running Python locally; no special hardware is required for this prototype.

## 6. Architecture
1. Presentation layer – HTML/Jinja templates, CSS and Bootstrap.
2. Application layer – Flask routes for registration, login, reporting, search, claims and administration.
3. Matching layer – TF-IDF converts report text to vectors; cosine similarity ranks candidates.
4. Data layer – SQLite stores users, reports and claims.

## 7. Main workflow
1. User registers and logs in.
2. User submits a lost or found report.
3. Flask validates fields and stores the report in SQLite.
4. User searches reports or opens a report detail page.
5. Matching module compares the report with open reports of the opposite type in the same category.
6. User reviews suggestions and may submit private claim evidence.
7. Administrator reviews claims and updates item status.

## 8. Database design
**Users:** id, name, email, password_hash, role, created_at.

**Items:** id, user_id, item_type, title, category, description, location, event_date, image_filename, status, created_at.

**Claims:** id, item_id, user_id, message, status, created_at.

Relationships: one user can submit many items; one item can receive many claims; each claim belongs to one user and one item.

## 9. AI matching methodology
The MVP combines title, description and location into a text string. `TfidfVectorizer` converts the two report descriptions into weighted term vectors. Cosine similarity measures the angle-based similarity between vectors. Candidate records are restricted to open reports of the opposite type and same category. A small location-overlap boost is applied. Results are sorted by score.

**Interpretation:** A score is a ranking signal, not a probability and not proof of ownership. Short or very different descriptions can produce weak scores. Human verification is mandatory.

## 10. Security and privacy considerations
- Passwords are stored as hashes, not plain text.
- Public reports should not contain private proof or sensitive identifying details.
- Claim messages are submitted privately and shown only in the admin review area in this prototype.
- Uploaded images are restricted by extension and size.
- Before real deployment, add CSRF protection, stronger role management, secure secret configuration, HTTPS, rate limiting, image-content validation, database backups and an institutional privacy review.

## 11. Testing approach
Unit tests cover the text similarity helper. Manual testing should cover account creation, login, report submission, upload validation, search, matching, claims and admin status updates. Record actual outcomes, screenshots and defects in the test log. No accuracy or performance results should be claimed before tests are run on a labeled dataset.

## 12. Challenges and solutions
| Challenge | Implemented response |
|---|---|
| Different wording for the same object | TF-IDF and cosine similarity rank text candidates |
| Too many unrelated reports | Filter by opposite report type and same category |
| False ownership claims | Private claim message and admin review workflow |
| Sensitive details exposed publicly | Guidance to keep unique proof private |
| Beginners need simple local setup | Flask + SQLite; no separate database server |

## 13. Limitations
The MVP uses text matching and simple metadata filters. It has not been connected to college identity systems, does not send notifications, and does not automatically verify item ownership. Matching performance depends on report quality and dataset size.

## 14. Future enhancements
- Image similarity using a suitable vision model.
- Email/in-app notifications.
- College SSO and role-based campus access.
- Admin audit history and analytics.
- Larger labeled dataset and formal evaluation of precision@k/recall@k.
- Deployment with HTTPS, backups and production security controls.
