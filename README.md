# Community Learning Hub Locator

A command-line, menu-driven Python application that helps users find,
add, and manage community learning hubs (e.g. libraries, tutoring
centers, study spaces) near them, backed by a database.

Built as a Peer Learning Project (PLP-2) for BSE Year 1, Trimester 2 —
African Leadership University.

## Team Members

| Member | Responsibility |
|---|---|
| Member 1 | Database Design |
| Member 2 | Registration & Authentication |
| Member 3 | Add & View Hubs |
| Member 4 | Search, Update & Delete Hubs |
| Member 5 | Testing & Documentation (QA) |
| Member 6 | Final Integration & Presentation |

## Features

- Find nearby learning hubs by location or name
- View resource availability per hub (Wi-Fi, books, study rooms, printing, charging, etc.)
- Search and filter hubs by resource, distance, hours, or accessibility
- Offline access to previously cached hub data
- Simulated data synchronization when connectivity is available
- Admin login (only admins can add, update, or delete hub records)
- Add / update / delete learning hub records (admin only)
- List all learning hubs

> Regular users do **not** register or log in — only admins do, in
> order to manage hub records. See the group's PLP-1 requirements spec
> for full details.

## Requirements

- Python 3.x
- SQLite (built-in via Python's `sqlite3` module) — no separate server needed

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ihirwe-promis/learning-hub-locator.git
   cd learning-hub-locator
   ```

2. Install dependencies:
   ```bash
   pip install mysql-connector-python python-dotenv
   ```

3. Create a `.env` file in the project root (do **not** commit this
   file) containing the database password:
   ```
   DB_PASSWORD=<ask a team member for the real password>
   ```

4. The database schema (`admins` and `hubs` tables) is hosted on Aiven
   MySQL cloud and should already be set up — no local setup needed.
   See `TESTING.md` for the exact schema.

## How to Run

```bash
python3 main.py
```

You'll be greeted with a menu. Example:

```
=== Community Learning Hub Locator ===
1. Find a Hub (search / filter / list)
2. Admin Login (to add, update, or delete hub records)
3. Sync Data
4. Exit
Choose an option:
```

_(Update this once the real menu text from `main.py` is finalized —
per the spec, the app is split into "find a hub" and "manage records,"
with manage records gated behind admin login.)_

## Project Structure

```
learning-hub-locator/
├── main.py          # Menu logic and program entry point
├── database.py      # Database setup and connection
├── test.py          # Test scripts
├── README.md
├── TESTING.md        # Test cases, results, and bug log
└── .gitignore
```

## Testing

See [TESTING.md](TESTING.md) for the full test case table, results, and
known issues.

## Known Issues (as of presentation)

- Search, Update, and Delete Hub currently fail — the code queries a
  column called `location`, but the database uses `address`. Fix in
  progress.
- Register/Login use a `users` table; the rest of the app uses
  `admins`. These should be reconciled.
- Filtering by resource/hours, offline access, and data sync are
  described in the requirements spec but not yet implemented.
- We used MySQL (Aiven cloud) instead of SQLite as originally specified
  in our PLP-1 document, since MySQL is what the group learned in
  class. We plan to explore SQLite as we learn it.

## Future Improvements

_(e.g. GPS-based distance search, hub ratings/reviews, admin roles, GUI
version)_