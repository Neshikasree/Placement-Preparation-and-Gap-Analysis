
import pytest

from gap_analysis.analyzer import (
    analyze_skills,
    get_recommendations
)

from gap_analysis.roles import JOB_ROLES

from gap_analysis.learning_content import (
    get_learning_content
)

from gap_analysis.roadmap import generate_roadmap

from gap_analysis.resume_analyzer import analyze_resume

from gap_analysis.quiz_history import (
    calculate_quiz_history
)


# Test learning content
def test_learning_content():

    for role in JOB_ROLES:

        for skill in JOB_ROLES[role]:

            content = get_learning_content(skill)

            assert content["topics"]
            assert content["task"]


# Test personalised recommendations
def test_recommendations():

    result = analyze_skills(
        "Python Developer",
        {
            "Python": 3,
            "SQL": 1,
            "Data Structures": 4,
            "Git": 2
        }
    )

    recommendations = get_recommendations(result)

    assert recommendations[0]["skill"] == "SQL"

    assert recommendations[0]["priority"] == "High"

    assert recommendations[0]["topics"]

    assert recommendations[0]["task"]


# Test four-week roadmap
def test_roadmap():

    result = analyze_skills(
        "Python Developer",
        {"Python": 2, "SQL": 1}
    )

    roadmap = generate_roadmap(result, weeks=4)

    assert len(roadmap) == 4

    assert roadmap[0]["week"] == 1

    assert roadmap[-1]["week"] == 4

    assert "reassessment" in roadmap[-1]["title"]


# Verify that no weak skills are omitted
@pytest.mark.parametrize("role", list(JOB_ROLES))
def test_roadmap_skill_coverage(role):

    result = analyze_skills(role, {})

    roadmap = generate_roadmap(result)

    covered = {
        activity["skill"]
        for week in roadmap
        for activity in week["activities"]
    }

    assert set(JOB_ROLES[role]).issubset(covered)


# Test roadmap for a fully prepared student
def test_roadmap_no_gaps():

    result = analyze_skills(
        "Python Developer",
        dict(JOB_ROLES["Python Developer"])
    )

    roadmap = generate_roadmap(result)

    assert len(roadmap) == 4

    assert roadmap[0]["title"] == "Maintain your skills"


# Test invalid preparation duration
def test_invalid_duration():

    result = analyze_skills("Python Developer", {})

    with pytest.raises(ValueError):
        generate_roadmap(result, weeks=1)


# Test resume analyzer
def test_resume_analyzer():

    result = analyze_resume(
        "I know Python and Git.",
        "Python Developer"
    )

    assert result["success"] is True

    assert result["match_percentage"] == 50

    assert "Python" in result["detected_skills"]

    assert "SQL" in result["missing_skills"]


# Test alternative skill names
def test_resume_aliases():

    result = analyze_resume(
        "Python, MySQL and GitHub",
        "Python Developer"
    )

    assert result["match_percentage"] == 75


# Test empty resume
def test_empty_resume():

    result = analyze_resume(
        "",
        "Python Developer"
    )

    assert result["success"] is False


# Test invalid career
def test_invalid_career():

    result = analyze_resume(
        "Python and SQL",
        "Invalid Career"
    )

    assert result["success"] is False


# Test quiz history
def test_quiz_history():

    attempts = [
        {
            "id": 1,
            "target_role": "Python Developer",
            "level": "Beginner",
            "score": 25,
            "created_at": "2026-11-01"
        },
        {
            "id": 2,
            "target_role": "Python Developer",
            "level": "Beginner",
            "score": 75,
            "created_at": "2026-11-02"
        }
    ]

    result = calculate_quiz_history(attempts)

    assert result["total_attempts"] == 2

    assert result["highest_score"] == 75

    assert result["average_score"] == 50

    assert result["improvement"] == 50


# Test empty quiz history
def test_empty_quiz_history():

    result = calculate_quiz_history([])

    assert result["total_attempts"] == 0

    assert result["history"] == []
