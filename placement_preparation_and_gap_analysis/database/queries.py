
"""Database functions used by Member 3's Flask routes (Member 2).

Every function has an optional db_path argument (used by the tests).
Functions raise ValueError with a clear message for bad input, so Flask can
catch it and show the message to the user.
"""

import sqlite3
from contextlib import closing

from gap_analysis.roles import JOB_ROLES, MAX_SKILL_LEVEL, MIN_SKILL_LEVEL

from .db import get_connection

# Every skill name that appears in at least one job role.
VALID_SKILLS = sorted({skill for skills in JOB_ROLES.values() for skill in skills})


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _clean_role(target_role):
    """Return the official role name (ignores case/extra spaces) or raise ValueError."""
    if isinstance(target_role, str):
        wanted = " ".join(target_role.split()).lower()
        for role_name in JOB_ROLES:
            if role_name.lower() == wanted:
                return role_name
    raise ValueError("Invalid job role: {!r}. Valid roles are: {}.".format(target_role, ", ".join(JOB_ROLES)))


def _clean_rating(skill, value):
    """Return a whole-number rating 0-5 or raise ValueError."""
    if isinstance(value, bool):
        raise ValueError("Invalid rating for {}: {!r}.".format(skill, value))
    if isinstance(value, str):
        try:
            value = float(value.strip())
        except ValueError:
            raise ValueError("Invalid rating for {}: {!r}.".format(skill, value))
    if not isinstance(value, (int, float)) or value != value:  # value != value is True only for NaN
        raise ValueError("Invalid rating for {}: {!r}.".format(skill, value))
    if not float(value).is_integer() or not MIN_SKILL_LEVEL <= value <= MAX_SKILL_LEVEL:
        raise ValueError("Rating for {} must be a whole number from {} to {}, got {!r}.".format(
            skill, MIN_SKILL_LEVEL, MAX_SKILL_LEVEL, value))
    return int(value)


def _row_to_dict(row):
    return dict(row) if row is not None else None


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

def add_student(name, email, target_role, db_path=None):
    """Register a student and return the new student id."""
    name = (name or "").strip() if isinstance(name, str) else ""
    email = (email or "").strip().lower() if isinstance(email, str) else ""
    if not name:
        raise ValueError("Name is required.")
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("A valid email address is required.")
    role = _clean_role(target_role)

    with closing(get_connection(db_path)) as connection:
        try:
            cursor = connection.execute(
                "INSERT INTO students (name, email, target_role) VALUES (?, ?, ?)",
                (name, email, role),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("A student with email {} is already registered.".format(email))
        return cursor.lastrowid


def get_student(student_id, db_path=None):
    """Return {"id", "name", "email", "target_role", "created_at"} or None."""
    with closing(get_connection(db_path)) as connection:
        row = connection.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        return _row_to_dict(row)


def get_student_by_email(email, db_path=None):
    """Return the student dictionary for this email, or None."""
    email = (email or "").strip().lower() if isinstance(email, str) else ""
    with closing(get_connection(db_path)) as connection:
        row = connection.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        return _row_to_dict(row)


def list_students(db_path=None):
    """Return a list of all students (oldest first)."""
    with closing(get_connection(db_path)) as connection:
        rows = connection.execute("SELECT * FROM students ORDER BY id").fetchall()
        return [dict(row) for row in rows]


def update_target_role(student_id, target_role, db_path=None):
    """Change a student's target role."""
    role = _clean_role(target_role)
    with closing(get_connection(db_path)) as connection:
        cursor = connection.execute("UPDATE students SET target_role = ? WHERE id = ?", (role, student_id))
        connection.commit()
        if cursor.rowcount == 0:
            raise ValueError("Student {} does not exist.".format(student_id))


# ---------------------------------------------------------------------------
# Assessments (skill ratings)
# ---------------------------------------------------------------------------

def save_assessment(student_id, skills, db_path=None):
    """Save skill ratings such as {"Python": 3, "SQL": 2}.

    A new rating for a skill replaces the old one. Either all ratings are
    saved or none (if one is invalid, nothing changes).
    """
    if not isinstance(skills, dict) or not skills:
        raise ValueError("skills must be a non-empty dictionary like {'Python': 3}.")

    cleaned = {}
    for skill, value in skills.items():
        if skill not in VALID_SKILLS:
            raise ValueError("Unknown skill: {!r}. Valid skills are: {}.".format(skill, ", ".join(VALID_SKILLS)))
        cleaned[skill] = _clean_rating(skill, value)

    with closing(get_connection(db_path)) as connection:
        if connection.execute("SELECT 1 FROM students WHERE id = ?", (student_id,)).fetchone() is None:
            raise ValueError("Student {} does not exist.".format(student_id))
        with connection:  # one transaction: commit on success, roll back on error
            for skill, rating in cleaned.items():
                connection.execute(
                    """INSERT INTO assessments (student_id, skill, rating) VALUES (?, ?, ?)
                       ON CONFLICT (student_id, skill)
                       DO UPDATE SET rating = excluded.rating, assessed_at = CURRENT_TIMESTAMP""",
                    (student_id, skill, rating),
                )


def get_student_skills(student_id, db_path=None):
    """Return the student's ratings as a plain dictionary, e.g. {"Python": 3, "SQL": 2}.

    This dictionary can be passed straight to analyze_skills(). Returns an
    empty dictionary if the student has no ratings yet.
    """
    with closing(get_connection(db_path)) as connection:
        rows = connection.execute(
            "SELECT skill, rating FROM assessments WHERE student_id = ? ORDER BY skill", (student_id,)
        ).fetchall()
        return {row["skill"]: row["rating"] for row in rows}


# ---------------------------------------------------------------------------
# Results (readiness score history)
# ---------------------------------------------------------------------------

def save_result(student_id, target_role, readiness_score, db_path=None):
    """Store a readiness score (0-100) for a student and return the result id."""
    role = _clean_role(target_role)
    if isinstance(readiness_score, bool) or not isinstance(readiness_score, (int, float)) \
            or not 0 <= readiness_score <= 100:
        raise ValueError("readiness_score must be a number from 0 to 100.")
    with closing(get_connection(db_path)) as connection:
        if connection.execute("SELECT 1 FROM students WHERE id = ?", (student_id,)).fetchone() is None:
            raise ValueError("Student {} does not exist.".format(student_id))
        cursor = connection.execute(
            "INSERT INTO results (student_id, target_role, readiness_score) VALUES (?, ?, ?)",
            (student_id, role, readiness_score),
        )
        connection.commit()
        return cursor.lastrowid


def get_results(student_id, db_path=None):
    """Return the student's saved results, newest first."""
    with closing(get_connection(db_path)) as connection:
        rows = connection.execute(
            "SELECT * FROM results WHERE student_id = ? ORDER BY id DESC", (student_id,)
        ).fetchall()
        return [dict(row) for row in rows]
=======
"""Database functions used by Member 3's Flask routes (Member 2).

Every function has an optional db_path argument (used by the tests).
Functions raise ValueError with a clear message for bad input, so Flask can
catch it and show the message to the user.
"""

import sqlite3
from contextlib import closing

from gap_analysis.roles import JOB_ROLES, MAX_SKILL_LEVEL, MIN_SKILL_LEVEL

from .db import get_connection

# Every skill name that appears in at least one job role.
VALID_SKILLS = sorted({skill for skills in JOB_ROLES.values() for skill in skills})


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _clean_role(target_role):
    """Return the official role name (ignores case/extra spaces) or raise ValueError."""
    if isinstance(target_role, str):
        wanted = " ".join(target_role.split()).lower()
        for role_name in JOB_ROLES:
            if role_name.lower() == wanted:
                return role_name
    raise ValueError("Invalid job role: {!r}. Valid roles are: {}.".format(target_role, ", ".join(JOB_ROLES)))


def _clean_rating(skill, value):
    """Return a whole-number rating 0-5 or raise ValueError."""
    if isinstance(value, bool):
        raise ValueError("Invalid rating for {}: {!r}.".format(skill, value))
    if isinstance(value, str):
        try:
            value = float(value.strip())
        except ValueError:
            raise ValueError("Invalid rating for {}: {!r}.".format(skill, value))
    if not isinstance(value, (int, float)) or value != value:  # value != value is True only for NaN
        raise ValueError("Invalid rating for {}: {!r}.".format(skill, value))
    if not float(value).is_integer() or not MIN_SKILL_LEVEL <= value <= MAX_SKILL_LEVEL:
        raise ValueError("Rating for {} must be a whole number from {} to {}, got {!r}.".format(
            skill, MIN_SKILL_LEVEL, MAX_SKILL_LEVEL, value))
    return int(value)


def _row_to_dict(row):
    return dict(row) if row is not None else None


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

def add_student(name, email, target_role, db_path=None):
    """Register a student and return the new student id."""
    name = (name or "").strip() if isinstance(name, str) else ""
    email = (email or "").strip().lower() if isinstance(email, str) else ""
    if not name:
        raise ValueError("Name is required.")
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("A valid email address is required.")
    role = _clean_role(target_role)

    with closing(get_connection(db_path)) as connection:
        try:
            cursor = connection.execute(
                "INSERT INTO students (name, email, target_role) VALUES (?, ?, ?)",
                (name, email, role),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("A student with email {} is already registered.".format(email))
        return cursor.lastrowid


def get_student(student_id, db_path=None):
    """Return {"id", "name", "email", "target_role", "created_at"} or None."""
    with closing(get_connection(db_path)) as connection:
        row = connection.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        return _row_to_dict(row)


def get_student_by_email(email, db_path=None):
    """Return the student dictionary for this email, or None."""
    email = (email or "").strip().lower() if isinstance(email, str) else ""
    with closing(get_connection(db_path)) as connection:
        row = connection.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        return _row_to_dict(row)


def list_students(db_path=None):
    """Return a list of all students (oldest first)."""
    with closing(get_connection(db_path)) as connection:
        rows = connection.execute("SELECT * FROM students ORDER BY id").fetchall()
        return [dict(row) for row in rows]


def update_target_role(student_id, target_role, db_path=None):
    """Change a student's target role."""
    role = _clean_role(target_role)
    with closing(get_connection(db_path)) as connection:
        cursor = connection.execute("UPDATE students SET target_role = ? WHERE id = ?", (role, student_id))
        connection.commit()
        if cursor.rowcount == 0:
            raise ValueError("Student {} does not exist.".format(student_id))


# ---------------------------------------------------------------------------
# Assessments (skill ratings)
# ---------------------------------------------------------------------------

def save_assessment(student_id, skills, db_path=None):
    """Save skill ratings such as {"Python": 3, "SQL": 2}.

    A new rating for a skill replaces the old one. Either all ratings are
    saved or none (if one is invalid, nothing changes).
    """
    if not isinstance(skills, dict) or not skills:
        raise ValueError("skills must be a non-empty dictionary like {'Python': 3}.")

    cleaned = {}
    for skill, value in skills.items():
        if skill not in VALID_SKILLS:
            raise ValueError("Unknown skill: {!r}. Valid skills are: {}.".format(skill, ", ".join(VALID_SKILLS)))
        cleaned[skill] = _clean_rating(skill, value)

    with closing(get_connection(db_path)) as connection:
        if connection.execute("SELECT 1 FROM students WHERE id = ?", (student_id,)).fetchone() is None:
            raise ValueError("Student {} does not exist.".format(student_id))
        with connection:  # one transaction: commit on success, roll back on error
            for skill, rating in cleaned.items():
                connection.execute(
                    """INSERT INTO assessments (student_id, skill, rating) VALUES (?, ?, ?)
                       ON CONFLICT (student_id, skill)
                       DO UPDATE SET rating = excluded.rating, assessed_at = CURRENT_TIMESTAMP""",
                    (student_id, skill, rating),
                )


def get_student_skills(student_id, db_path=None):
    """Return the student's ratings as a plain dictionary, e.g. {"Python": 3, "SQL": 2}.

    This dictionary can be passed straight to analyze_skills(). Returns an
    empty dictionary if the student has no ratings yet.
    """
    with closing(get_connection(db_path)) as connection:
        rows = connection.execute(
            "SELECT skill, rating FROM assessments WHERE student_id = ? ORDER BY skill", (student_id,)
        ).fetchall()
        return {row["skill"]: row["rating"] for row in rows}


# ---------------------------------------------------------------------------
# Results (readiness score history)
# ---------------------------------------------------------------------------

def save_result(student_id, target_role, readiness_score, db_path=None):
    """Store a readiness score (0-100) for a student and return the result id."""
    role = _clean_role(target_role)
    if isinstance(readiness_score, bool) or not isinstance(readiness_score, (int, float)) \
            or not 0 <= readiness_score <= 100:
        raise ValueError("readiness_score must be a number from 0 to 100.")
    with closing(get_connection(db_path)) as connection:
        if connection.execute("SELECT 1 FROM students WHERE id = ?", (student_id,)).fetchone() is None:
            raise ValueError("Student {} does not exist.".format(student_id))
        cursor = connection.execute(
            "INSERT INTO results (student_id, target_role, readiness_score) VALUES (?, ?, ?)",
            (student_id, role, readiness_score),
        )
        connection.commit()
        return cursor.lastrowid


def get_results(student_id, db_path=None):
    """Return the student's saved results, newest first."""
    with closing(get_connection(db_path)) as connection:
        rows = connection.execute(
            "SELECT * FROM results WHERE student_id = ? ORDER BY id DESC", (student_id,)
        ).fetchall()
        return [dict(row) for row in rows]
>>>>>>> c4b8fdf7f9c8cceb95af9e45525f2e45c3a95d65
