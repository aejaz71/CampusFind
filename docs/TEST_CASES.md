# CampusFind – Test Cases

Record the actual result and evidence after running each test. Expected results are not test results.

| ID | Test | Steps | Expected result | Actual result |
|---|---|---|---|---|
| TC01 | Register | Submit name, unique email, password | Account created | Pending |
| TC02 | Duplicate registration | Register same email again | Duplicate warning | Pending |
| TC03 | Login | Use correct credentials | Dashboard opens | Pending |
| TC04 | Invalid login | Use wrong password | Error shown | Pending |
| TC05 | Lost report | Submit complete lost report | Report saved | Pending |
| TC06 | Found report | Submit complete found report | Report saved | Pending |
| TC07 | Required fields | Submit incomplete report | Validation message | Pending |
| TC08 | Search | Search by title/location | Matching open reports shown | Pending |
| TC09 | Category filter | Select category | Only that category shown | Pending |
| TC10 | AI matching | Create similar lost/found reports in same category | Candidate appears with similarity score | Pending |
| TC11 | Claim | Submit private message of 10+ characters | Claim saved | Pending |
| TC12 | Admin review | Log in as admin and review claim | Claim status can be changed | Pending |
| TC13 | Item status | Admin changes item status | New status is saved | Pending |
| TC14 | Image type | Upload unsupported file type | Upload rejected | Pending |
| TC15 | Image size | Upload image over 4 MB | Upload rejected | Pending |

## Matching evaluation
Create a small dataset of known corresponding lost/found pairs and non-matches. For each lost report, check whether the correct found report is ranked in the first result (Top-1) or first three results (Top-3).

Top-k match rate = number of queries with a true match in top k / total queries × 100.

Report dataset size, labeling method, date and results. Do not present a small classroom sample as general real-world accuracy.
