"""Skill gap analysis and preparation recommendations (Member 1).

Public functions (the interface shared with Member 2 and Member 3):
    analyze_skills(target_role, current_skills) -> dict
    get_recommendations(analysis_result)        -> list of dicts
"""

import math

from .roles import JOB_ROLES, MAX_SKILL_LEVEL, MIN_SKILL_LEVEL

# ---------------------------------------------------------------------------
# Recommendation text
# ---------------------------------------------------------------------------

GENERAL_ADVICE = {
    "High": "Learn the fundamentals and practise daily.",
    "Medium": "Practise intermediate exercises and complete small projects.",
    "Low": "Revise the concepts and solve advanced problems.",
    "None": "Maintain your current skill level.",
}

# skill -> {priority: suggestion}
SKILL_SUGGESTIONS = {
    "Python": {
        "High": "Follow a beginner Python course (variables, loops, functions, lists, dictionaries) and code for 1 hour every day.",
        "Medium": "Build small projects such as a to-do app or a number-guessing game, and practise file handling and OOP.",
        "Low": "Revise decorators, generators and list comprehensions, and solve medium/hard Python problems.",
        "None": "Keep practising by building a project or solving one problem a week.",
    },
    "SQL": {
        "High": "Learn SELECT, WHERE, ORDER BY, INSERT, UPDATE and DELETE; practise on a small SQLite database.",
        "Medium": "Practise JOINs, GROUP BY, HAVING and aggregate functions with real tables.",
        "Low": "Revise subqueries, indexes and window functions, and solve interview-style SQL questions.",
        "None": "Keep SQL fresh by writing a few queries every week.",
    },
    "HTML": {
        "High": "Learn page structure, headings, lists, links, images, tables and forms; build a simple personal page.",
        "Medium": "Practise semantic tags, accessible forms and multi-page layouts.",
        "Low": "Revise accessibility, SEO basics and semantic structure by rebuilding a real website.",
        "None": "Keep HTML sharp by building or improving a page now and then.",
    },
    "CSS": {
        "High": "Learn selectors, the box model, colours and fonts; style a simple page from scratch.",
        "Medium": "Practise Flexbox, Grid and responsive layouts with small page clones.",
        "Low": "Revise animations, CSS variables and mobile-first design; recreate a polished website.",
        "None": "Keep practising by styling a new page layout occasionally.",
    },
    "JavaScript": {
        "High": "Learn variables, functions, arrays, objects and DOM basics; make a small interactive page.",
        "Medium": "Practise DOM events, fetch/API calls and small projects like a calculator or quiz app.",
        "Low": "Revise closures, promises, async/await and ES6+ features; solve JavaScript challenges.",
        "None": "Keep building small interactive features to stay in practice.",
    },
    "Data Structures": {
        "High": "Learn arrays, strings, lists, stacks and queues; solve 2 easy problems daily.",
        "Medium": "Practise linked lists, hash maps, trees and sorting/searching on medium problems.",
        "Low": "Revise graphs, heaps and dynamic programming; solve timed medium/hard problems.",
        "None": "Solve a few problems every week to maintain your level.",
    },
    "Git": {
        "High": "Learn git init, add, commit, status and log; create a GitHub repository and push to it.",
        "Medium": "Practise branches, merging, pull requests and resolving simple merge conflicts.",
        "Low": "Revise rebase, stash and clean commit history; contribute to a team repository.",
        "None": "Keep using Git for every project you build.",
    },
    "Problem Solving": {
        "High": "Practise basic logic puzzles and easy coding problems; learn to break a problem into steps.",
        "Medium": "Solve medium coding problems regularly and learn patterns like two pointers and recursion.",
        "Low": "Take timed contests and mock interviews; explain your solutions out loud.",
        "None": "Keep solving a few varied problems every week.",
    },
}

DEFAULT_SUGGESTION = "Look for a beginner-friendly course or tutorial on this skill."


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _find_role(target_role):
    """Return the official role name matching target_role (ignores case and
    extra spaces), or None if there is no match."""
    if not isinstance(target_role, str):
        return None
    wanted = " ".join(target_role.split()).lower()
    for role_name in JOB_ROLES:
        if role_name.lower() == wanted:
            return role_name
    return None


def _clean_rating(value):
    """Convert one rating to a number.

    Returns (number, None) if valid, or (None, error_message) if invalid.
    Accepts ints, floats and numeric strings such as "3" (HTML forms send
    strings). Booleans, NaN, text and values outside 0-5 are rejected.
    """
    if isinstance(value, bool):
        return None, "rating must be a number, not True/False"
    if isinstance(value, str):
        try:
            value = float(value.strip())
        except ValueError:
            return None, "rating must be a number"
    if not isinstance(value, (int, float)):
        return None, "rating must be a number"
    if math.isnan(value) or math.isinf(value):
        return None, "rating must be a real number"
    if value < MIN_SKILL_LEVEL or value > MAX_SKILL_LEVEL:
        return None, "rating must be between {} and {}".format(MIN_SKILL_LEVEL, MAX_SKILL_LEVEL)
    if float(value).is_integer():
        value = int(value)
    return value, None


def _error_result(target_role, errors):
    """Build the structure returned when the input cannot be analysed."""
    return {
        "success": False,
        "target_role": target_role,
        "readiness_score": None,
        "total_required_points": None,
        "total_achieved_points": None,
        "skill_gaps": [],
        "missing_skills": [],
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Public function 1: gap analysis
# ---------------------------------------------------------------------------

def analyze_skills(target_role, current_skills):
    """Compare a student's skills with the requirements of a job role.

    Args:
        target_role: e.g. "Python Developer".
        current_skills: dict such as {"Python": 3, "SQL": 2}. Skills the role
            does not need are ignored. Skills that are missing count as 0.

    Returns:
        A dictionary. It always contains the key "success".
        On success:
            {
              "success": True,
              "target_role": "Python Developer",
              "readiness_score": 68.75,
              "total_required_points": 16,
              "total_achieved_points": 11,
              "skill_gaps": [
                  {"skill": "Python", "required_level": 5, "current_level": 3,
                   "gap": 2, "status": "Needs improvement", "missing": False},
                  ...
              ],
              "missing_skills": ["Git"],
              "errors": []
            }
        On bad input: "success" is False, "errors" lists what went wrong,
        and readiness_score is None. This function never raises for bad input.
    """
    role_name = _find_role(target_role)
    if role_name is None:
        valid = ", ".join(JOB_ROLES)
        return _error_result(
            target_role,
            ["Invalid job role: {!r}. Valid roles are: {}.".format(target_role, valid)],
        )

    if not isinstance(current_skills, dict):
        return _error_result(role_name, ["current_skills must be a dictionary of skill ratings."])

    requirements = JOB_ROLES[role_name]
    skill_gaps = []
    missing_skills = []
    errors = []
    total_required = 0
    total_achieved = 0

    for skill, required in requirements.items():
        raw_value = current_skills.get(skill)

        if raw_value is None:  # not supplied at all
            current = 0
            is_missing = True
            missing_skills.append(skill)
        else:
            current, problem = _clean_rating(raw_value)
            if problem:
                errors.append("Invalid rating for {}: {!r} ({}).".format(skill, raw_value, problem))
                continue
            is_missing = False

        gap = max(required - current, 0)
        achieved = min(current, required)  # extra skill above requirement is not counted
        total_required += required
        total_achieved += achieved

        skill_gaps.append({
            "skill": skill,
            "required_level": required,
            "current_level": current,
            "gap": gap,
            "status": "Met" if gap == 0 else "Needs improvement",
            "missing": is_missing,
        })

    if errors:
        return _error_result(role_name, errors)

    readiness = round(total_achieved / total_required * 100, 2) if total_required else 0.0

    return {
        "success": True,
        "target_role": role_name,
        "readiness_score": readiness,
        "total_required_points": total_required,
        "total_achieved_points": total_achieved,
        "skill_gaps": skill_gaps,
        "missing_skills": missing_skills,
        "errors": [],
    }


# ---------------------------------------------------------------------------
# Public function 2: recommendations
# ---------------------------------------------------------------------------

def _priority_for_gap(gap):
    if gap >= 3:
        return "High"
    if gap >= 2:
        return "Medium"
    if gap > 0:
        return "Low"
    return "None"


def get_recommendations(analysis_result):
    """Create preparation advice from the result of analyze_skills().

    Returns a list of dictionaries, biggest gap first:
        [{"skill": "Python", "gap": 3, "priority": "High",
          "advice": "Learn the fundamentals and practise daily.",
          "suggestion": "Follow a beginner Python course ..."}, ...]
    Returns an empty list if the analysis failed or is not a valid result.
    """
    if not isinstance(analysis_result, dict) or not analysis_result.get("success"):
        return []

    recommendations = []
    for item in analysis_result.get("skill_gaps", []):
        skill = item["skill"]
        gap = item["gap"]
        priority = _priority_for_gap(gap)
        tips = SKILL_SUGGESTIONS.get(skill, {})
        recommendations.append({
            "skill": skill,
            "gap": gap,
            "priority": priority,
            "advice": GENERAL_ADVICE[priority],
            "suggestion": tips.get(priority, DEFAULT_SUGGESTION),
        })

    recommendations.sort(key=lambda r: r["gap"], reverse=True)  # stable sort
    return recommendations
