
"""Automated tests for PlaceReady adaptive assessments."""

import pytest

from gap_analysis.roles import JOB_ROLES

from adaptive_assessment import (
    AdaptiveAssessment,
    QUESTION_BANK,
    LEVELS,
    PASS_THRESHOLD,
)


def correct_answers(assessment):
    bank = {
        q["id"]: q["answer"]
        for q in QUESTION_BANK
    }

    return {
        q["id"]: bank[q["id"]]
        for q in assessment.get_questions()
    }


def wrong_answers(assessment):
    correct = correct_answers(assessment)

    return {
        q["id"]: next(
            option for option in q["options"]
            if option != correct[q["id"]]
        )
        for q in assessment.get_questions()
    }


# QUESTION BANK TESTS

def test_unique_question_ids():
    ids = [q["id"] for q in QUESTION_BANK]
    assert len(ids) == len(set(ids))


def test_valid_question_options():
    for q in QUESTION_BANK:
        assert len(q["options"]) == 4
        assert len(set(q["options"])) == 4
        assert q["answer"] in q["options"]
        assert q["level"] in LEVELS


def test_six_career_roles():
    assert len(JOB_ROLES) == 6


@pytest.mark.parametrize("role", list(JOB_ROLES))
def test_question_coverage(role):
    for skill in JOB_ROLES[role]:
        for level in LEVELS:
            assert any(
                q["skill"] == skill
                and q["level"] == level
                for q in QUESTION_BANK
            )


# ASSESSMENT INITIALIZATION TESTS

@pytest.mark.parametrize("role", list(JOB_ROLES))
def test_assessment_starts_at_beginner(role):
    assessment = AdaptiveAssessment(role)

    assert assessment.current_level == "Beginner"
    assert assessment.completed is False
    assert assessment.get_questions()


def test_invalid_role():
    with pytest.raises(ValueError):
        AdaptiveAssessment("Invalid Role")


def test_answers_are_hidden():
    assessment = AdaptiveAssessment("Python Developer")

    for q in assessment.get_questions():
        assert "answer" not in q


# SCORING AND PROGRESSION TESTS

def test_perfect_score():
    assessment = AdaptiveAssessment("Python Developer")

    response = assessment.submit_answers(
        correct_answers(assessment)
    )

    assert response["result"]["score"] == 100
    assert response["result"]["passed"] is True


def test_zero_score():
    assessment = AdaptiveAssessment("Python Developer")

    response = assessment.submit_answers(
        wrong_answers(assessment)
    )

    assert response["result"]["score"] == 0
    assert response["result"]["passed"] is False
    assert assessment.completed is True


def test_beginner_to_intermediate():
    assessment = AdaptiveAssessment("Python Developer")

    response = assessment.submit_answers(
        correct_answers(assessment)
    )

    assert response["next_level"] == "Intermediate"


def test_intermediate_to_advanced():
    assessment = AdaptiveAssessment("Python Developer")

    assessment.submit_answers(
        correct_answers(assessment)
    )

    response = assessment.submit_answers(
        correct_answers(assessment)
    )

    assert response["next_level"] == "Advanced"


def test_exact_80_percent_threshold():
    assessment = AdaptiveAssessment("Software Developer")

    answers = correct_answers(assessment)

    q = assessment.get_questions()[0]

    answers[q["id"]] = next(
        option for option in q["options"]
        if option != answers[q["id"]]
    )

    response = assessment.submit_answers(answers)

    assert PASS_THRESHOLD == 80
    assert response["result"]["score"] == 80
    assert response["result"]["passed"] is True


def test_below_threshold():
    assessment = AdaptiveAssessment("Software Developer")

    answers = correct_answers(assessment)

    for q in assessment.get_questions()[:2]:
        answers[q["id"]] = next(
            option for option in q["options"]
            if option != answers[q["id"]]
        )

    response = assessment.submit_answers(answers)

    assert response["result"]["score"] == 60
    assert response["result"]["passed"] is False
    assert assessment.completed is True


# FINAL REPORT TESTS

@pytest.mark.parametrize("role", list(JOB_ROLES))
def test_complete_assessment(role):
    assessment = AdaptiveAssessment(role)

    while not assessment.completed:
        assessment.submit_answers(
            correct_answers(assessment)
        )

    report = assessment.generate_report()

    assert report["estimated_level"] == "Advanced"
    assert report["overall_score"] == 100
    assert len(report["history"]) == 3
    assert report["weak_skills"] == []


def test_weak_skills():
    assessment = AdaptiveAssessment("Data Analyst")

    assessment.submit_answers(
        wrong_answers(assessment)
    )

    report = assessment.generate_report()

    assert report["overall_score"] == 0

    assert set(report["weak_skills"]) == set(
        JOB_ROLES["Data Analyst"]
    )


def test_recommendations():
    assessment = AdaptiveAssessment("Python Developer")

    assessment.submit_answers(
        wrong_answers(assessment)
    )

    report = assessment.generate_report()

    assert report["recommendations"]

    for item in report["recommendations"]:
        assert item["skill"]
        assert item["suggestion"]
        assert item["priority"] == "High"


def test_failed_intermediate():
    assessment = AdaptiveAssessment("Python Developer")

    assessment.submit_answers(
        correct_answers(assessment)
    )

    assessment.submit_answers(
        wrong_answers(assessment)
    )

    report = assessment.generate_report()

    assert report["estimated_level"] == "Beginner"
    assert report["overall_score"] == 50
    assert len(report["history"]) == 2


# INPUT VALIDATION TESTS

def test_missing_answers():
    assessment = AdaptiveAssessment("Python Developer")

    with pytest.raises(ValueError):
        assessment.submit_answers({})

    assert assessment.history == []


def test_invalid_answer():
    assessment = AdaptiveAssessment("Python Developer")

    answers = correct_answers(assessment)
    question_id = next(iter(answers))

    answers[question_id] = "Invalid option"

    with pytest.raises(ValueError):
        assessment.submit_answers(answers)

    assert assessment.history == []


def test_extra_answers():
    assessment = AdaptiveAssessment("Python Developer")

    answers = correct_answers(assessment)
    answers["unknown_id"] = "Unknown answer"

    with pytest.raises(ValueError):
        assessment.submit_answers(answers)


def test_submission_after_completion():
    assessment = AdaptiveAssessment("Python Developer")

    answers = wrong_answers(assessment)

    assessment.submit_answers(answers)

    with pytest.raises(ValueError):
        assessment.submit_answers(answers)


def test_report_before_completion():
    assessment = AdaptiveAssessment("Python Developer")

    with pytest.raises(ValueError):
        assessment.generate_report()


def test_old_answers_rejected():
    assessment = AdaptiveAssessment("Python Developer")

    answers = correct_answers(assessment)

    assessment.submit_answers(answers)

    with pytest.raises(ValueError):
        assessment.submit_answers(answers)


# INDEPENDENCE AND DATA INTEGRITY TESTS

def test_independent_assessments():
    first = AdaptiveAssessment("Python Developer")
    second = AdaptiveAssessment("Python Developer")

    first.submit_answers(correct_answers(first))

    assert first.current_level == "Intermediate"
    assert second.current_level == "Beginner"
    assert second.history == []


def test_question_bank_unchanged():
    original = [
        list(q["options"])
        for q in QUESTION_BANK
    ]

    AdaptiveAssessment("Python Developer")

    assert original == [
        q["options"]
        for q in QUESTION_BANK
    ]


def test_completed_assessment_has_no_questions():
    assessment = AdaptiveAssessment("Python Developer")

    assessment.submit_answers(
        wrong_answers(assessment)
    )

    assert assessment.get_questions() == []
