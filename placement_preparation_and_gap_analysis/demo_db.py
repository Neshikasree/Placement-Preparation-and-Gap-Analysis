"""Standalone demo for Member 2's database module (no Flask needed).

Run from the project root:   python demo_db.py
It uses a separate file, demo_placement.db, which is deleted and recreated
every time, so your real placement.db is never touched.
"""

import os

from database import (add_student, get_results, get_student, get_student_skills,
                      init_db, list_students, save_assessment, save_result)
from gap_analysis import analyze_skills, get_recommendations

DEMO_DB = "demo_placement.db"


def main():
    if os.path.exists(DEMO_DB):
        os.remove(DEMO_DB)
    init_db(DEMO_DB)

    student_id = add_student("Asha Kumar", "asha@example.com", "Python Developer", db_path=DEMO_DB)
    print("Registered student id:", student_id)

    save_assessment(student_id, {"Python": 3, "SQL": 2, "Data Structures": 4}, db_path=DEMO_DB)
    skills = get_student_skills(student_id, db_path=DEMO_DB)
    print("Saved skills:", skills)

    student = get_student(student_id, db_path=DEMO_DB)
    result = analyze_skills(student["target_role"], skills)
    print("Readiness score:", result["readiness_score"])
    for rec in get_recommendations(result)[:2]:
        print("  [{}] {}: {}".format(rec["priority"], rec["skill"], rec["advice"]))

    save_result(student_id, student["target_role"], result["readiness_score"], db_path=DEMO_DB)
    print("Result history:", [r["readiness_score"] for r in get_results(student_id, db_path=DEMO_DB)])
    print("All students:", [s["name"] for s in list_students(db_path=DEMO_DB)])

    try:
        add_student("Duplicate", "asha@example.com", "Web Developer", db_path=DEMO_DB)
    except ValueError as error:
        print("Duplicate email rejected ->", error)

    os.remove(DEMO_DB)
    print("Demo finished.")


if __name__ == "__main__":
    main()
