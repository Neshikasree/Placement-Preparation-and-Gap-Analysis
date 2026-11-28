

"""Sample career skill requirements for PlaceReady.

These requirements are illustrative values for educational
placement preparation. They are not official industry standards.
"""


# --------------------------------------------------
# SKILL RATING SCALE
# --------------------------------------------------

MIN_SKILL_LEVEL = 0
MAX_SKILL_LEVEL = 5

SKILL_LEVEL_LABELS = {
    0: "Not learned",
    1: "Beginner",
    2: "Basic",
    3: "Intermediate",
    4: "Advanced",
    5: "Strong",
}


# --------------------------------------------------
# CAREER REQUIREMENTS
# --------------------------------------------------

JOB_ROLES = {

    # EXISTING ROLE 1

    "Python Developer": {
        "Python": 5,
        "SQL": 4,
        "Data Structures": 4,
        "Git": 3,
    },

    # EXISTING ROLE 2

    "Web Developer": {
        "HTML": 5,
        "CSS": 4,
        "JavaScript": 4,
        "Git": 3,
    },

    # EXISTING ROLE 3

    "Software Developer": {
        "Python": 4,
        "SQL": 4,
        "Data Structures": 5,
        "Problem Solving": 5,
        "Git": 3,
    },

    # NEW ROLE 4

    "Data Analyst": {
        "Python": 4,
        "SQL": 5,
        "Statistics": 4,
        "Excel": 4,
        "Pandas": 4,
        "Data Visualization": 4,
    },

    # NEW ROLE 5

    "AI/ML Engineer": {
        "Python": 5,
        "Statistics": 4,
        "Linear Algebra": 4,
        "Machine Learning": 5,
        "NumPy": 4,
        "Pandas": 4,
        "Deep Learning": 3,
        "Git": 3,
    },

    # NEW ROLE 6

    "Cybersecurity Analyst": {
        "Networking": 5,
        "Linux": 4,
        "Cybersecurity Fundamentals": 5,
        "Python": 3,
        "Cryptography": 3,
        "Security Monitoring": 4,
        "Incident Response": 4,
    },
}


# --------------------------------------------------
# CAREER DESCRIPTIONS
# --------------------------------------------------

ROLE_DESCRIPTIONS = {

    "Python Developer":
        "Develop applications, automation tools and backend "
        "systems using Python.",

    "Web Developer":
        "Build responsive, accessible and interactive websites "
        "and web applications.",

    "Software Developer":
        "Design, develop, test and maintain software applications.",

    "Data Analyst":
        "Analyse datasets, identify patterns and communicate "
        "insights using reports and visualizations.",

    "AI/ML Engineer":
        "Develop and evaluate artificial intelligence and "
        "machine learning models.",

    "Cybersecurity Analyst":
        "Monitor and protect computer systems, assess security "
        "risks and respond to security incidents.",
}


# --------------------------------------------------
# CAREER CATEGORIES
# --------------------------------------------------

ROLE_CATEGORIES = {
    "Python Developer": "Software Development",
    "Web Developer": "Web Development",
    "Software Developer": "Software Development",
    "Data Analyst": "Data Science and Analytics",
    "AI/ML Engineer": "Artificial Intelligence",
    "Cybersecurity Analyst": "Information Security",
}
