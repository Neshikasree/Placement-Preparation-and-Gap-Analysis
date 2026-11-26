"""Unit tests for the gap_analysis package. Run with:  python -m pytest -v"""

import pytest

from gap_analysis import analyze_skills, get_recommendations
from gap_analysis.roles import JOB_ROLES


def perfect_skills(role):
    return dict(JOB_ROLES[role])


def gap_of(result, skill):
    return next(i for i in result["skill_gaps"] if i["skill"] == skill)["gap"]


# --- readiness score -------------------------------------------------------

def test_perfect_readiness_score():
    result = analyze_skills("Python Developer", perfect_skills("Python Developer"))
    assert result["success"] is True
    assert result["readiness_score"] == 100
    assert all(item["gap"] == 0 for item in result["skill_gaps"])


def test_partial_readiness_score():
    # Required: Python 5, SQL 4, DS 4, Git 3 = 16 points. Achieved 3+2+4+0 = 9.
    skills = {"Python": 3, "SQL": 2, "Data Structures": 4, "Git": 0}
    result = analyze_skills("Python Developer", skills)
    assert result["total_required_points"] == 16
    assert result["total_achieved_points"] == 9
    assert result["readiness_score"] == pytest.approx(56.25)


def test_zero_skills_gives_zero_score():
    result = analyze_skills("Web Developer", {})
    assert result["readiness_score"] == 0


# --- gaps ------------------------------------------------------------------

def test_skill_gap_calculation():
    skills = {"Python": 2, "SQL": 4, "Data Structures": 3, "Git": 1}
    result = analyze_skills("Python Developer", skills)
    assert gap_of(result, "Python") == 3
    assert gap_of(result, "SQL") == 0
    assert gap_of(result, "Data Structures") == 1
    assert gap_of(result, "Git") == 2


def test_result_structure():
    result = analyze_skills("Web Developer", {"HTML": 5})
    for key in ("success", "target_role", "readiness_score", "skill_gaps", "errors"):
        assert key in result
    for key in ("skill", "required_level", "current_level", "gap"):
        assert key in result["skill_gaps"][0]


# --- invalid input ---------------------------------------------------------

def test_invalid_job_role():
    result = analyze_skills("Astronaut", {"Python": 3})
    assert result["success"] is False
    assert result["readiness_score"] is None
    assert "Invalid job role" in result["errors"][0]


@pytest.mark.parametrize("bad_role", [None, 123, ""])
def test_non_string_or_empty_role(bad_role):
    assert analyze_skills(bad_role, {})["success"] is False


def test_role_name_ignores_case_and_spaces():
    result = analyze_skills("  python developer ", perfect_skills("Python Developer"))
    assert result["success"] is True
    assert result["target_role"] == "Python Developer"


@pytest.mark.parametrize("bad_value", [-1, 6, 5.5, "abc", True, float("nan")])
def test_invalid_skill_ratings(bad_value):
    skills = perfect_skills("Python Developer")
    skills["Python"] = bad_value
    result = analyze_skills("Python Developer", skills)
    assert result["success"] is False
    assert result["readiness_score"] is None
    assert "Python" in result["errors"][0]


def test_skills_not_a_dictionary():
    assert analyze_skills("Python Developer", [1, 2, 3])["success"] is False


def test_numeric_strings_are_accepted():
    # HTML forms send strings
    result = analyze_skills("Python Developer", {"Python": "5", "SQL": "4", "Data Structures": "4", "Git": "3"})
    assert result["readiness_score"] == 100


# --- missing skills --------------------------------------------------------

def test_missing_skill_counts_as_zero():
    result = analyze_skills("Python Developer", {"Python": 5, "SQL": 4, "Data Structures": 4})
    assert result["success"] is True
    assert result["missing_skills"] == ["Git"]
    assert gap_of(result, "Git") == 3
    assert result["readiness_score"] == pytest.approx(13 / 16 * 100)


def test_none_rating_counts_as_missing():
    result = analyze_skills("Web Developer", {"HTML": None})
    assert "HTML" in result["missing_skills"]


def test_extra_skills_are_ignored():
    skills = perfect_skills("Web Developer")
    skills["Cooking"] = 5
    result = analyze_skills("Web Developer", skills)
    assert result["readiness_score"] == 100


# --- skill above requirement -----------------------------------------------

def test_skill_above_requirement_is_capped():
    # Git required 3. Rating 5 must count as only 3 achieved points.
    skills = {"Python": 5, "SQL": 4, "Data Structures": 4, "Git": 5}
    result = analyze_skills("Python Developer", skills)
    assert result["readiness_score"] == 100
    assert gap_of(result, "Git") == 0


def test_surplus_cannot_cover_other_gaps():
    # Python 5 (cap 5), everything else 0 -> 5 / 16
    result = analyze_skills("Python Developer", {"Python": 5})
    assert result["readiness_score"] == pytest.approx(5 / 16 * 100)


# --- recommendations -------------------------------------------------------

def test_recommendation_levels():
    skills = {"Python": 2, "SQL": 2, "Data Structures": 3, "Git": 3}  # gaps 3, 2, 1, 0
    recs = {r["skill"]: r for r in get_recommendations(analyze_skills("Python Developer", skills))}
    assert recs["Python"]["priority"] == "High"
    assert "fundamentals" in recs["Python"]["advice"]
    assert recs["SQL"]["priority"] == "Medium"
    assert "small projects" in recs["SQL"]["advice"]
    assert recs["Data Structures"]["priority"] == "Low"
    assert "Revise" in recs["Data Structures"]["advice"]
    assert recs["Git"]["priority"] == "None"
    assert "Maintain" in recs["Git"]["advice"]


def test_recommendations_sorted_by_biggest_gap():
    skills = {"Python": 4, "SQL": 0, "Data Structures": 3, "Git": 3}
    recs = get_recommendations(analyze_skills("Python Developer", skills))
    gaps = [r["gap"] for r in recs]
    assert gaps == sorted(gaps, reverse=True)
    assert recs[0]["skill"] == "SQL"


def test_recommendations_have_skill_specific_text():
    recs = get_recommendations(analyze_skills("Web Developer", {}))
    assert all(r["suggestion"] for r in recs)
    html = next(r for r in recs if r["skill"] == "HTML")
    css = next(r for r in recs if r["skill"] == "CSS")
    assert html["suggestion"] != css["suggestion"]


@pytest.mark.parametrize("bad", [None, {}, "text", analyze_skills("Nope", {})])
def test_recommendations_for_invalid_analysis(bad):
    assert get_recommendations(bad) == []


# --- all three roles -------------------------------------------------------

@pytest.mark.parametrize("role", ["Python Developer", "Web Developer", "Software Developer"])
def test_all_roles_perfect_and_empty(role):
    perfect = analyze_skills(role, perfect_skills(role))
    empty = analyze_skills(role, {})
    assert perfect["readiness_score"] == 100
    assert empty["readiness_score"] == 0
    assert len(perfect["skill_gaps"]) == len(JOB_ROLES[role])
    assert len(get_recommendations(perfect)) == len(JOB_ROLES[role])


def test_role_requirements_match_specification():
    assert JOB_ROLES["Python Developer"] == {"Python": 5, "SQL": 4, "Data Structures": 4, "Git": 3}
    assert JOB_ROLES["Web Developer"] == {"HTML": 5, "CSS": 4, "JavaScript": 4, "Git": 3}
    assert JOB_ROLES["Software Developer"] == {
        "Python": 4, "SQL": 4, "Data Structures": 5, "Problem Solving": 5, "Git": 3}
