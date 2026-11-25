"""Unit tests for the database package. Run with:  python -m pytest -v"""

import pytest

from database import (
    add_student, get_results, get_student, get_student_by_email, get_student_skills,
    init_db, list_students, save_assessment, save_result, update_target_role,
)
from gap_analysis import analyze_skills


def make_db(tmp_path):
    """Create a fresh empty database file for one test."""
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


def test_init_db_can_run_twice(tmp_path):
    path = make_db(tmp_path)
    init_db(path)  # must not fail


def test_add_and_get_student(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("Asha", "Asha@Example.com", "python developer", db_path=db)
    student = get_student(student_id, db_path=db)
    assert student["name"] == "Asha"
    assert student["email"] == "asha@example.com"       # lower-cased
    assert student["target_role"] == "Python Developer"  # official spelling


def test_get_missing_student_returns_none(tmp_path):
    db = make_db(tmp_path)
    assert get_student(999, db_path=db) is None
    assert get_student_by_email("nobody@example.com", db_path=db) is None


def test_duplicate_email_rejected(tmp_path):
    db = make_db(tmp_path)
    add_student("A", "a@example.com", "Web Developer", db_path=db)
    with pytest.raises(ValueError):
        add_student("B", "A@example.com", "Web Developer", db_path=db)


@pytest.mark.parametrize("name,email,role", [
    ("", "a@example.com", "Web Developer"),
    ("A", "not-an-email", "Web Developer"),
    ("A", "a@example.com", "Astronaut"),
    (None, "a@example.com", "Web Developer"),
])
def test_invalid_student_input(tmp_path, name, email, role):
    db = make_db(tmp_path)
    with pytest.raises(ValueError):
        add_student(name, email, role, db_path=db)
    assert list_students(db_path=db) == []


def test_list_students_and_find_by_email(tmp_path):
    db = make_db(tmp_path)
    add_student("A", "a@example.com", "Web Developer", db_path=db)
    add_student("B", "b@example.com", "Software Developer", db_path=db)
    assert [s["name"] for s in list_students(db_path=db)] == ["A", "B"]
    assert get_student_by_email(" B@example.com ", db_path=db)["name"] == "B"


def test_update_target_role(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Web Developer", db_path=db)
    update_target_role(student_id, "Software Developer", db_path=db)
    assert get_student(student_id, db_path=db)["target_role"] == "Software Developer"
    with pytest.raises(ValueError):
        update_target_role(999, "Software Developer", db_path=db)


def test_save_and_read_assessment(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    save_assessment(student_id, {"Python": 3, "SQL": 2}, db_path=db)
    assert get_student_skills(student_id, db_path=db) == {"Python": 3, "SQL": 2}


def test_new_rating_replaces_old_rating(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    save_assessment(student_id, {"Python": 1}, db_path=db)
    save_assessment(student_id, {"Python": 4, "Git": 2}, db_path=db)
    assert get_student_skills(student_id, db_path=db) == {"Git": 2, "Python": 4}


def test_numeric_strings_are_saved_as_numbers(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    save_assessment(student_id, {"Python": "3"}, db_path=db)
    assert get_student_skills(student_id, db_path=db) == {"Python": 3}


@pytest.mark.parametrize("bad_value", [-1, 6, 2.5, "abc", None, True])
def test_invalid_ratings_rejected(tmp_path, bad_value):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    with pytest.raises(ValueError):
        save_assessment(student_id, {"Python": bad_value}, db_path=db)
    assert get_student_skills(student_id, db_path=db) == {}


def test_one_bad_rating_saves_nothing(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    with pytest.raises(ValueError):
        save_assessment(student_id, {"Python": 3, "SQL": 99}, db_path=db)
    assert get_student_skills(student_id, db_path=db) == {}


def test_unknown_skill_and_unknown_student_rejected(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    with pytest.raises(ValueError):
        save_assessment(student_id, {"Cooking": 3}, db_path=db)
    with pytest.raises(ValueError):
        save_assessment(999, {"Python": 3}, db_path=db)
    with pytest.raises(ValueError):
        save_assessment(student_id, {}, db_path=db)


def test_student_with_no_ratings_gets_empty_dict(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    assert get_student_skills(student_id, db_path=db) == {}


def test_save_and_get_results_newest_first(tmp_path):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    save_result(student_id, "Python Developer", 40.5, db_path=db)
    save_result(student_id, "Python Developer", 62.5, db_path=db)
    results = get_results(student_id, db_path=db)
    assert [r["readiness_score"] for r in results] == [62.5, 40.5]


@pytest.mark.parametrize("bad_score", [-1, 101, "high", None])
def test_invalid_result_score_rejected(tmp_path, bad_score):
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    with pytest.raises(ValueError):
        save_result(student_id, "Python Developer", bad_score, db_path=db)


def test_database_output_works_with_member1_analyzer(tmp_path):
    """Integration: database -> analyze_skills (no Flask needed)."""
    db = make_db(tmp_path)
    student_id = add_student("A", "a@example.com", "Python Developer", db_path=db)
    save_assessment(student_id, {"Python": 3, "SQL": 2, "Data Structures": 4}, db_path=db)  # Git not rated
    student = get_student(student_id, db_path=db)
    result = analyze_skills(student["target_role"], get_student_skills(student_id, db_path=db))
    assert result["success"] is True
    assert result["readiness_score"] == pytest.approx(56.25)
    assert result["missing_skills"] == ["Git"]
