
"""Gap analysis package (Member 1).

Member 3 can import everything needed with:
    from gap_analysis import analyze_skills, get_recommendations
"""

from .analyzer import analyze_skills, get_recommendations
from .roles import JOB_ROLES, SKILL_LEVEL_LABELS

__all__ = ["analyze_skills", "get_recommendations", "JOB_ROLES", "SKILL_LEVEL_LABELS"]
