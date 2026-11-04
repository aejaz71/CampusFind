# CampusFind – Implementation & Midway Progress (Review 2)

> Update this document with the team's actual progress and evidence before submission. Do not mark a feature complete until it has been run and demonstrated.

## 1. Basic implementation of core functionalities
The MVP source code includes:
- Registration and login with hashed passwords.
- Lost/found report creation and optional image upload.
- Search by keywords, category and report type.
- SQLite persistence for users, items and claims.
- Text-based candidate ranking with TF-IDF and cosine similarity.
- Private claim submission.
- Admin claim review and item status updates.

**Evidence to attach:** screenshots of registration, dashboard, report form, search results, matching results and admin page.

## 2. Partial working model / prototype
Demonstration sequence:
1. Register a normal user.
2. Log in and submit a found-item report, e.g. “Black leather wallet found near library entrance”.
3. Register/log in as a second user and submit the corresponding lost report.
4. Open the lost report and show the ranked possible match.
5. Submit a private claim message of at least 10 characters.
6. Log in as `admin@campusfind.local` and review the claim.
7. Change the item status to returned/resolved.

The prototype is a decision-support system. The team must manually verify ownership.

## 3. Code quality, structure and documentation review
The code is separated into:
- `app.py`: Flask routes, database access and matching logic.
- `templates/`: user interface pages.
- `static/`: CSS and uploaded images.
- `docs/`: project documentation, tests, progress and team contribution records.
- `tests/`: automated unit tests.

Review items before submission:
- Remove unused files and test accounts.
- Use meaningful names and comments.
- Keep secrets out of source control.
- Confirm all dependencies are listed in `requirements.txt`.
- Add screenshots and update this report with actual test results.

## 4. Challenges faced and solutions applied
| Challenge | Solution in this prototype |
|---|---|
| Reports can use different words | TF-IDF + cosine similarity ranks textual candidates |
| Search results can be noisy | Filter by report type and category |
| False claims are possible | Private proof message and admin review |
| Reports need persistence | SQLite database |
| User privacy matters | Do not expose claim proof in public item pages |

Add any additional challenges your team actually faced: __________________________

## 5. Testing approach and preliminary results
Automated test:
`python -m unittest discover -s tests -v`

Manual test cases are listed in `TEST_CASES.md`.

**Actual test execution date:** __________________
**Tests passed:** ______ / ______
**Tests failed:** ______
**Known defects:** ______________________________

Do not enter assumed accuracy percentages. To evaluate matching, prepare labeled lost/found pairs and report Top-1 or Top-3 match rate after running the experiment.

## 6. Timeline alignment and adjustments
The original plan in Review 1 was:
- Review 1: 12–14 Oct 2026 – proposal, scope, architecture, feasibility.
- Review 2: 4–6 Nov 2026 – core website, database, reporting workflow.
- Review 3: 1–3 Dec 2026 – matching, testing, refinements, documentation.
- Department exhibition: 9 Dec 2026.
- College exhibition: 17 Dec 2026.

**Midway status:** The implementation package now provides the core website, database schema, reporting workflow and text-matching module. The team must run it locally and record evidence before claiming successful demonstration.

**Suggested adjustment:** Use the period after Review 2 to validate all workflows, build a small consent-based labeled sample dataset, improve UI and matching, complete test evidence, and rehearse the demo before Review 3.

## 7. GitHub and documentation
The repository should contain source code, README, requirements, docs, tests, review presentations and non-sensitive demo screenshots. Do not commit passwords, `.env`, private claim data, real student personal information, or the local SQLite database.

## 8. Team preparation
Each member should explain their actual contribution and demonstrate one module. Complete `TEAM_CONTRIBUTIONS.md` with verified work; the suggested division from Review 1 is not proof of completed work.
