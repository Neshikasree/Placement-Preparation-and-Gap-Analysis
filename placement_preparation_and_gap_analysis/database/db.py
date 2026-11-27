<<<<<<< HEAD
"""SQLite connection and table creation (Member 2)."""

import os
import sqlite3

# The database file is created in the project root unless the environment
# variable PLACEMENT_DB_PATH points somewhere else.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.environ.get("PLACEMENT_DB_PATH", os.path.join(PROJECT_ROOT, "placement.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    target_role TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assessments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL,
    skill       TEXT NOT NULL,
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 0 AND 5),
    assessed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, skill),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    target_role     TEXT NOT NULL,
    readiness_score REAL NOT NULL,
    created_at      TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);
"""


def get_connection(db_path=None):
    """Open a connection. Rows can be read like dictionaries (row["name"])."""
    connection = sqlite3.connect(db_path or DEFAULT_DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")  # SQLite needs this on every connection
    return connection


def init_db(db_path=None):
    """Create the tables if they do not exist yet. Safe to call many times."""
    connection = get_connection(db_path)
    try:
        connection.executescript(SCHEMA)
        connection.commit()
    finally:
        connection.close()
=======
"""SQLite connection and table creation (Member 2)."""

import os
import sqlite3

# The database file is created in the project root unless the environment
# variable PLACEMENT_DB_PATH points somewhere else.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.environ.get("PLACEMENT_DB_PATH", os.path.join(PROJECT_ROOT, "placement.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    target_role TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assessments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL,
    skill       TEXT NOT NULL,
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 0 AND 5),
    assessed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, skill),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    target_role     TEXT NOT NULL,
    readiness_score REAL NOT NULL,
    created_at      TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);
"""


def get_connection(db_path=None):
    """Open a connection. Rows can be read like dictionaries (row["name"])."""
    connection = sqlite3.connect(db_path or DEFAULT_DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")  # SQLite needs this on every connection
    return connection


def init_db(db_path=None):
    """Create the tables if they do not exist yet. Safe to call many times."""
    connection = get_connection(db_path)
    try:
        connection.executescript(SCHEMA)
        connection.commit()
    finally:
        connection.close()
>>>>>>> c4b8fdf7f9c8cceb95af9e45525f2e45c3a95d65
