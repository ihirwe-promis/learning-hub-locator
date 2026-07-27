# Testing Documentation — Community Learning Hub Locator

**Tested by:** Member 5 (QA & Testing)
**Last updated:** July 26, 2026 (night before presentation)

## 1. Purpose

This document tracks manual testing of every feature in the Community
Learning Hub Locator CLI application. Each test case records what was
tested, how, what was expected, and what actually happened.

## 2. How to Run the App (for testing)

```bash
git clone https://github.com/ihirwe-promis/learning-hub-locator.git
cd learning-hub-locator
git checkout <branch-name>   # e.g. member2-user-authentication, member3-add-view-hubs, member4-search-update-delete
pip install python-dotenv
```

Create a `.env` file in the project root (not committed to git) containing:
```
DB_PASSWORD=<real password, shared privately by Member 1/Promis>
```

Then run:
```bash
python3 main.py
```
(or `python3 hub_management.py` to test Member 3's Add/View Hub functions directly, without the full menu.)

## 3. Confirmed Database Schema (as of tonight)

```sql
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE hubs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    resources TEXT,
    hours VARCHAR(100),
    contact VARCHAR(100),
    sync_status VARCHAR(50) DEFAULT 'pending',
    updated_by INT,
    FOREIGN KEY (updated_by) REFERENCES admins(id)
);
```

This matches the group's PLP-1 requirements spec (SQLite was originally
specified; the group opted for MySQL/Aiven cloud DB instead, since that
is what was taught in class — flagged as an intentional deviation from
the original spec, worth mentioning if asked at presentation).

**Known open issue:** the Register/Login code (`register_user()`,
`login()`) currently creates and uses a table called `users`, not
`admins`. This is a mismatch against the corrected schema above and has
been flagged to the group but is not yet resolved as of this writing.

## 4. Test Case Results

| Test ID | Feature | Owner | Test Case Description | Expected Result | Actual Result | Status | Notes |
|---|---|---|---|---|---|---|---|
| TC-01 | App startup | Member 1 | App connects to DB and starts without error | No errors on launch | Confirmed on `main` branch | **Pass** | |
| TC-02 | Database schema | Member 1 | `hubs`/`admins` tables match spec | Columns match Section 3 above | Initially failed ("unknown column address") — fixed after Promis applied corrected schema | **Pass** (after fix) | See BUG-03 |
| TC-03 | Register (valid) | Member 2 | New user can register with unique username/password | "registered successfully" confirmation | Confirmed working | **Pass** | Uses `users` table, not `admins` — see open issue above |
| TC-04 | Login (valid) | Member 2 | Registered user can log in with correct credentials | "Welcome back" message | Confirmed working | **Pass** | |
| TC-05 | Login (invalid) | Member 2 | Wrong password/username rejected | Error message, access denied | Not yet tested | **Not tested** | |
| TC-06 | Register (duplicate) | Member 2 | Registering existing username is rejected | "username already taken" message | Not yet tested | **Not tested** | |
| TC-07 | Menu navigation | Member 1/3/4/6 | Menu displays and routes correctly | All options route, exit works | Confirmed on all branches tested | **Pass** | Early version of `main.py` on `member3` branch was initially missing the `menu()` call entirely — fixed, see BUG-01 |
| TC-08 | Add Hub (valid) | Member 3 | Admin can add a new hub with all fields | Hub saved, confirmation with Hub ID shown | Confirmed working after DB password + schema + admin row were fixed | **Pass** | See BUG-02, BUG-03, BUG-05 |
| TC-09 | Add Hub (missing name) | Member 3 | Missing required field rejected | Validation error, no bad record saved | Confirmed — validation runs after all fields entered (not immediately), but correctly rejects | **Pass** | Minor UX note: validates at the end, not per-field |
| TC-10 | View Hubs (empty DB) | Member 3 | Empty hub list handled gracefully | "No learning hubs found" message | Confirmed | **Pass** | |
| TC-11 | View Hubs (with data) | Member 3 | Hubs display with all correct fields | All fields shown correctly | Confirmed — added hub displayed correctly | **Pass** | |
| TC-12 | Search Hub (no match) | Member 4 | Non-existent search term handled gracefully | "No hubs found" message | Confirmed | **Pass** | |
| TC-13 | Search Hub (match) | Member 4 | Valid search returns correct hub(s) | Matching hub(s) shown | **Fails** — code searches `location` column, but schema uses `address` | **Fail** | See BUG-04, reported to Member 4 |
| TC-14 | Update Hub (invalid ID) | Member 4 | Non-numeric ID rejected | "Invalid Hub ID" message | Confirmed | **Pass** | |
| TC-15 | Update Hub (valid ID) | Member 4 | Existing hub can be updated | Hub updated, confirmation shown | **Fails** — same `location`/`address` column mismatch as Search | **Fail** | See BUG-04 |
| TC-16 | Delete Hub (invalid ID) | Member 4 | Non-numeric ID rejected | "Invalid Hub ID" message | Confirmed | **Pass** | |
| TC-17 | Delete Hub (valid ID) | Member 4 | Existing hub can be deleted | Hub removed, confirmation shown | **Fails** — same column mismatch | **Fail** | See BUG-04 |
| TC-18 | Filter by resource/hours | Member 4 | Filtering hubs by resource type or hours | Filtered results shown | Not built yet | **Not built** | |
| TC-19 | Offline access | Member 1/4 | Search/view work without internet | Cached data returned | Not built yet | **Not built** | |
| TC-20 | Data sync (simulated) | Member 1/4 | Sync updates `sync_status` field | Field updates, no crash | Not built yet | **Not built** | |
| TC-21 | Final integration | Member 6 | All members' branches merged into one working `main.py` | Single app with all features working together | Not done yet | **Pending** | Depends on schema/bug fixes above being resolved first |

## 5. Bug Log

| Bug ID | Related Test ID | Description | Severity | Status | Assigned To |
|---|---|---|---|---|---|
| BUG-01 | TC-07 | Early `main.py` on `member3-add-view-hubs` branch defined `menu()` but never called it — app did nothing on run | High | **Fixed** | Member 3 |
| BUG-02 | TC-08 | DB password was hardcoded in `database.py` and committed to a public repo | Medium | **Fixed** (moved to `.env`, not committed) | Member 1 |
| BUG-03 | TC-02, TC-08 | Real database's `hubs` table didn't match code's expected columns ("unknown column 'address'") — different members had assumed different schemas | High | **Fixed** | Member 1 (Promis) applied corrected schema |
| BUG-04 | TC-13, TC-15, TC-17 | `search_hub()`, `update_hub()`, `delete_hub()` in Member 4's code query a column called `location`, but the real schema uses `address` | High | **Open** | Member 4 (Djay) |
| BUG-05 | TC-08 | `add_hub()` initially failed with a foreign key error — hardcoded `updated_by = 1` referenced a non-existent admin | High | **Fixed** (admin row manually added; long-term fix still needed to use real logged-in admin's ID instead of hardcoded placeholder) | Member 3 / integration (Member 6) |
| BUG-06 | — | `register_user()`/`login()` use a table called `users`, not `admins` as the corrected schema specifies | Medium | **Open** | Member 2 |

## 6. Sign-off (status as of tonight, before presentation)

- [x] Core features tested at least once (Register, Login, Add Hub, View Hubs)
- [ ] Search/Update/Delete Hub — blocked on BUG-04 (location vs address column fix)
- [x] Critical bugs found and reported to relevant members
- [ ] All known bugs fixed — 2 still open (BUG-04, BUG-06)
- [x] README installation steps drafted (see README.md)
- [ ] Final integrated `main.py` tested end-to-end — pending Member 6's integration