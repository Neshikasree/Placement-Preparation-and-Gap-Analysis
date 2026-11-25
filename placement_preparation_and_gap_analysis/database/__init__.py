"""Database package (Member 2).

Member 3 can import everything needed with:
    from database import init_db, add_student, save_assessment, get_student_skills
"""

from .db import DEFAULT_DB_PATH, get_connection, init_db
from .queries import (
    add_student,
    get_results,
    get_student,
    get_student_by_email,
    get_student_skills,
    list_students,
    save_assessment,
    save_result,
    update_target_role,
)

__all__ = [
    "DEFAULT_DB_PATH", "get_connection", "init_db",
    "add_student", "get_student", "get_student_by_email", "list_students",
    "update_target_role", "save_assessment", "get_student_skills",
    "save_result", "get_results",
]
