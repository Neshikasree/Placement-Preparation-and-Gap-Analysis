"""Tests for the Flask app (Member 3). Run with:  python -m pytest -v"""

import pytest

from app import create_app, readiness_level
from gap_analysis.roles import JOB_ROLES


def make_client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def text(response):
    return response.get_data(as_text=True)


def register(client, role="Python Developer", email="asha@example.com", name="Asha"):
    return client.post("/register", data={"name": name, "email": email, "target_role": role})


def test_home_page_lists_all_roles(tmp_path):
    client = make_client(tmp_path)
    response = client.get("/")
    assert response.status_code == 200
    for role in JOB_ROLES:
        assert role in text(response)


def test_registration_redirects_to_assessment(tmp_path):
    client = make_client(tmp_path)
    response = register(client)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/assessment/1")


def test_invalid_registration_shows_error(tmp_path):
    client = make_client(tmp_path)
    response = client.post("/register", data={"name": "", "email": "bad", "target_role": "Astronaut"})
    assert response.status_code == 400
    assert "Name is required" in text(response)


def test_duplicate_email_shows_error(tmp_path):
    client = make_client(tmp_path)
    register(client)
    response = register(client)
    assert response.status_code == 400
    assert "already registered" in text(response)


@pytest.mark.parametrize("role", ["Python Developer", "Web Developer", "Software Developer"])
def test_assessment_page_shows_role_skills(tmp_path, role):
    client = make_client(tmp_path)
    register(client, role=role)
    page = text(client.get("/assessment/1"))
    for skill in JOB_ROLES[role]:
        assert skill in page


def test_full_flow_shows_correct_score(tmp_path):
    client = make_client(tmp_path)
    register(client)
    response = client.post("/assessment/1", data={"Python": "3", "SQL": "2", "Data Structures": "4", "Git": "0"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/results/1")

    page = text(client.get("/results/1"))
    assert "56.2%" in page or "56.3%" in page      # 9 of 16 points
    assert "Making progress" in page
    assert "Preparation recommendations" in page
    assert "Learn the fundamentals" in page         # Git gap is 3


def test_perfect_scores_give_100_percent(tmp_path):
    client = make_client(tmp_path)
    register(client, role="Web Developer")
    client.post("/assessment/1", data={"HTML": "5", "CSS": "4", "JavaScript": "4", "Git": "3"})
    page = text(client.get("/results/1"))
    assert "100.0%" in page
    assert "Placement ready" in page


def test_invalid_rating_shows_error_and_saves_nothing(tmp_path):
    client = make_client(tmp_path)
    register(client)
    response = client.post("/assessment/1", data={"Python": "9"})
    assert response.status_code == 400
    assert "Rating for Python" in text(response)
    # nothing was saved, so results redirect back to the assessment
    assert client.get("/results/1").status_code == 302


def test_results_without_assessment_redirects(tmp_path):
    client = make_client(tmp_path)
    register(client)
    response = client.get("/results/1")
    assert response.status_code == 302
    assert "/assessment/1" in response.headers["Location"]


def test_unknown_student_gives_404(tmp_path):
    client = make_client(tmp_path)
    assert client.get("/assessment/99").status_code == 404
    assert client.get("/results/99").status_code == 404
    assert "Page Not Found" in text(client.get("/results/99"))


def test_students_page(tmp_path):
    client = make_client(tmp_path)
    assert "No students registered yet" in text(client.get("/students"))
    register(client)
    page = text(client.get("/students"))
    assert "Asha" in page
    assert "Start assessment" in page


def test_retaking_assessment_keeps_score_history(tmp_path):
    client = make_client(tmp_path)
    register(client)
    client.post("/assessment/1", data={"Python": "1", "SQL": "1", "Data Structures": "1", "Git": "1"})
    client.post("/assessment/1", data={"Python": "5", "SQL": "4", "Data Structures": "4", "Git": "3"})
    page = text(client.get("/results/1"))
    assert "100.0%" in page
    assert "Your previous scores" in page


@pytest.mark.parametrize("score,label", [(100, "Placement ready"), (65, "Almost ready"),
                                          (45, "Making progress"), (10, "Just getting started")])
def test_readiness_level_labels(score, label):
    assert readiness_level(score)[0] == label
