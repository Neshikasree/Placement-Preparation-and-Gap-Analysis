
LEARNING_CONTENT = {
    "Python": {
        "topics": [
            "Variables and data types",
            "Functions and loops",
            "Object-oriented programming",
            "File handling"
        ],
        "task": "Build a student management program."
    },

    "SQL": {
        "topics": [
            "SELECT and WHERE",
            "JOIN operations",
            "GROUP BY",
            "Subqueries"
        ],
        "task": "Practice 10 queries using a sample database."
    },

    "Data Structures": {
        "topics": [
            "Arrays and lists",
            "Stacks and queues",
            "Trees",
            "Searching and sorting"
        ],
        "task": "Solve five data structure problems."
    },

    "Git": {
        "topics": [
            "Repositories",
            "Commits",
            "Branches",
            "Merging"
        ],
        "task": "Create a repository and merge a feature branch."
    },

    "HTML": {
        "topics": [
            "Semantic elements",
            "Forms",
            "Tables",
            "Page structure"
        ],
        "task": "Create a personal portfolio webpage."
    },

    "CSS": {
        "topics": [
            "Selectors",
            "Box model",
            "Flexbox and Grid",
            "Responsive design"
        ],
        "task": "Design a responsive portfolio page."
    },

    "JavaScript": {
        "topics": [
            "Variables and functions",
            "Arrays and objects",
            "DOM manipulation",
            "Events"
        ],
        "task": "Build an interactive to-do list."
    },

    "Problem Solving": {
        "topics": [
            "Logical reasoning",
            "Algorithm design",
            "Time complexity",
            "Debugging"
        ],
        "task": "Solve five programming challenges."
    },

    "Statistics": {
        "topics": [
            "Mean and median",
            "Probability",
            "Standard deviation",
            "Correlation"
        ],
        "task": "Analyse a sample dataset."
    },

    "Excel": {
        "topics": [
            "Formulas",
            "Lookup functions",
            "Pivot tables",
            "Charts"
        ],
        "task": "Create a student marks dashboard."
    },

    "Pandas": {
        "topics": [
            "DataFrames",
            "Data cleaning",
            "Filtering",
            "Grouping"
        ],
        "task": "Clean and analyse a CSV dataset."
    },

    "Data Visualization": {
        "topics": [
            "Bar charts",
            "Line charts",
            "Scatter plots",
            "Data storytelling"
        ],
        "task": "Create charts from a public dataset."
    },

    "Linear Algebra": {
        "topics": [
            "Vectors",
            "Matrices",
            "Matrix multiplication",
            "Linear transformations"
        ],
        "task": "Practice vector and matrix operations."
    },

    "Machine Learning": {
        "topics": [
            "Supervised learning",
            "Unsupervised learning",
            "Regression",
            "Model evaluation"
        ],
        "task": "Study and compare basic prediction models."
    },

    "NumPy": {
        "topics": [
            "Arrays",
            "Indexing",
            "Broadcasting",
            "Numerical operations"
        ],
        "task": "Perform calculations using NumPy arrays."
    },

    "Deep Learning": {
        "topics": [
            "Neural networks",
            "Activation functions",
            "Training concepts",
            "Overfitting"
        ],
        "task": "Draw and explain a simple neural network."
    },

    "Networking": {
        "topics": [
            "OSI model",
            "TCP/IP",
            "DNS",
            "HTTP and HTTPS"
        ],
        "task": "Draw a basic computer network diagram."
    },

    "Linux": {
        "topics": [
            "File system",
            "Basic commands",
            "File permissions",
            "Process management"
        ],
        "task": "Practice basic file management commands."
    },

    "Cybersecurity Fundamentals": {
        "topics": [
            "Security principles",
            "Authentication",
            "Access control",
            "Phishing awareness"
        ],
        "task": "Prepare a cybersecurity awareness checklist."
    },

    "Cryptography": {
        "topics": [
            "Encryption concepts",
            "Symmetric encryption",
            "Asymmetric encryption",
            "Hashing"
        ],
        "task": "Compare encryption and hashing concepts."
    },

    "Security Monitoring": {
        "topics": [
            "System logs",
            "Security alerts",
            "Anomaly detection",
            "Monitoring fundamentals"
        ],
        "task": "Review fictional security event logs."
    },

    "Incident Response": {
        "topics": [
            "Incident identification",
            "Containment concepts",
            "Recovery",
            "Incident documentation"
        ],
        "task": "Prepare a sample incident response report."
    }
}


def get_learning_content(skill):
    """Return learning topics and practice tasks for a skill."""

    content = LEARNING_CONTENT.get(skill, {
        "topics": ["Study the fundamentals of " + skill],
        "task": "Complete a beginner-friendly practice exercise."
    })

    return {
        "topics": list(content["topics"]),
        "task": content["task"]
    }
