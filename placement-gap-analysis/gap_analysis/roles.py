"""Sample job role requirements for the Placement Preparation project.

NOTE: These values are sample numbers for our college project.
They are NOT official industry standards.
"""

MIN_SKILL_LEVEL = 0
MAX_SKILL_LEVEL = 5

# The 0-5 rating scale used everywhere in the project.
SKILL_LEVEL_LABELS = {
    0: "Not learned",
    1: "Beginner",
    2: "Basic",
    3: "Intermediate",
    4: "Advanced",
    5: "Strong",
}

# role name -> {skill name: required level (0-5)}
JOB_ROLES = {
    "Python Developer": {
        "Python": 5,
        "SQL": 4,
        "Data Structures": 4,
        "Git": 3,
    },
    "Web Developer": {
        "HTML": 5,
        "CSS": 4,
        "JavaScript": 4,
        "Git": 3,
    },
    "Software Developer": {
        "Python": 4,
        "SQL": 4,
        "Data Structures": 5,
        "Problem Solving": 5,
        "Git": 3,
    },
}
