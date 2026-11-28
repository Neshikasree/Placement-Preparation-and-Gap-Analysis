
"""PlaceReady adaptive assessment question bank."""

LEVELS = ("Beginner", "Intermediate", "Advanced")

QUESTION_BANK = []


def add(skill, level, question, correct, wrong1, wrong2, wrong3):
    QUESTION_BANK.append({
        "id": f"Q{len(QUESTION_BANK) + 1:03d}",
        "skill": skill,
        "level": level,
        "question": question,
        "options": [correct, wrong1, wrong2, wrong3],
        "answer": correct,
    })


# ==================================================
# PYTHON
# ==================================================

add("Python", "Beginner",
    "Which Python data type is mutable?",
    "List", "Tuple", "String", "Integer")

add("Python", "Intermediate",
    "What does a Python generator use to return values lazily?",
    "yield", "break", "continue", "import")

add("Python", "Advanced",
    "What is the main purpose of a context manager?",
    "Manage resource setup and cleanup",
    "Compile Python into Java",
    "Remove all exceptions",
    "Create global variables")


# ==================================================
# SQL
# ==================================================

add("SQL", "Beginner",
    "Which SQL keyword retrieves data?",
    "SELECT", "DELETE", "DROP", "UPDATE")

add("SQL", "Intermediate",
    "Which clause filters grouped results?",
    "HAVING", "WHERE", "ORDER BY", "LIMIT")

add("SQL", "Advanced",
    "Which window function assigns consecutive row numbers?",
    "ROW_NUMBER()", "SUM()", "COUNT()", "LOWER()")


# ==================================================
# DATA STRUCTURES
# ==================================================

add("Data Structures", "Beginner",
    "Which structure follows FIFO?",
    "Queue", "Stack", "Tree", "Set")

add("Data Structures", "Intermediate",
    "What is the time complexity of binary search on a sorted array?",
    "O(log n)", "O(n)", "O(n squared)", "O(2^n)")

add("Data Structures", "Advanced",
    "Which structure is commonly used to implement a priority queue?",
    "Heap", "Unsorted array only", "String", "Boolean")


# ==================================================
# GIT
# ==================================================

add("Git", "Beginner",
    "Which command displays the working tree status?",
    "git status", "git init", "git clone", "git push")

add("Git", "Intermediate",
    "Which command temporarily saves uncommitted changes?",
    "git stash", "git log", "git fetch", "git tag")

add("Git", "Advanced",
    "Which command finds the commit that introduced a bug using binary search?",
    "git bisect", "git status", "git remote", "git init")


# ==================================================
# HTML
# ==================================================

add("HTML", "Beginner",
    "Which HTML element creates a hyperlink?",
    "<a>", "<p>", "<div>", "<h1>")

add("HTML", "Intermediate",
    "Which attribute provides alternative text for an image?",
    "alt", "href", "class", "width")

add("HTML", "Advanced",
    "Which element represents a standalone piece of content?",
    "<article>", "<br>", "<span>", "<b>")


# ==================================================
# CSS
# ==================================================

add("CSS", "Beginner",
    "Which property changes text colour?",
    "color", "padding", "margin", "display")

add("CSS", "Intermediate",
    "Which layout system is designed for rows and columns together?",
    "CSS Grid", "Float only", "Text align", "Border radius")

add("CSS", "Advanced",
    "Which selector normally has the highest specificity?",
    "#header", ".header", "header", "*")


# ==================================================
# JAVASCRIPT
# ==================================================

add("JavaScript", "Beginner",
    "Which keyword declares a block-scoped variable that can be reassigned?",
    "let", "const", "def", "int")

add("JavaScript", "Intermediate",
    "Which method converts a JSON string into a JavaScript value?",
    "JSON.parse()", "JSON.stringify()", "JSON.create()", "JSON.read()")

add("JavaScript", "Advanced",
    "What does a closure allow a function to retain?",
    "Access to its lexical environment",
    "Access to every browser password",
    "Unlimited memory",
    "Automatic network access")


# ==================================================
# PROBLEM SOLVING
# ==================================================

add("Problem Solving", "Beginner",
    "What should you do first when solving a programming problem?",
    "Understand the requirements",
    "Write random code",
    "Ignore the inputs",
    "Delete the test cases")

add("Problem Solving", "Intermediate",
    "What does divide and conquer do?",
    "Splits a problem into smaller subproblems",
    "Removes all input",
    "Avoids using algorithms",
    "Always uses a database")

add("Problem Solving", "Advanced",
    "When is dynamic programming especially useful?",
    "When subproblems overlap and optimal substructure exists",
    "When no computation is needed",
    "Only when sorting strings",
    "Only when displaying HTML")


# ==================================================
# STATISTICS
# ==================================================

add("Statistics", "Beginner",
    "What is the mean of 2, 4 and 6?",
    "4", "2", "6", "12")

add("Statistics", "Intermediate",
    "Which measure describes how spread out values are?",
    "Standard deviation", "Mode", "Median", "Sample name")

add("Statistics", "Advanced",
    "What is a Type I error in hypothesis testing?",
    "Rejecting a true null hypothesis",
    "Failing to reject a false null hypothesis",
    "Calculating the mean",
    "Increasing the sample size")


# ==================================================
# EXCEL
# ==================================================

add("Excel", "Beginner",
    "Which function adds numbers?",
    "SUM", "COUNT", "MAX", "MIN")

add("Excel", "Intermediate",
    "Which feature summarizes large tables interactively?",
    "PivotTable", "Font colour", "Page margin", "Spell check")

add("Excel", "Advanced",
    "Which tool supports importing and transforming data?",
    "Power Query", "WordArt", "Page Break", "Print Preview")


# ==================================================
# PANDAS
# ==================================================

add("Pandas", "Beginner",
    "Which Pandas structure represents tabular data?",
    "DataFrame", "Integer", "Boolean", "Tuple only")

add("Pandas", "Intermediate",
    "Which method groups rows for aggregation?",
    "groupby()", "print()", "append()", "len()")

add("Pandas", "Advanced",
    "Which merge type preserves every row from the left table?",
    "Left join", "Inner join", "Right join", "Cross join")


# ==================================================
# DATA VISUALIZATION
# ==================================================

add("Data Visualization", "Beginner",
    "Which chart is suitable for comparing categories?",
    "Bar chart", "Paragraph", "Source code", "File tree")

add("Data Visualization", "Intermediate",
    "Which chart is useful for showing correlation between two numeric variables?",
    "Scatter plot", "Pie chart", "Single text label", "File icon")

add("Data Visualization", "Advanced",
    "Why should a standard bar chart generally start its value axis at zero?",
    "To avoid misleading comparisons of bar lengths",
    "To increase file size",
    "To remove category labels",
    "To change the underlying data")


# ==================================================
# LINEAR ALGEBRA
# ==================================================

add("Linear Algebra", "Beginner",
    "What is an ordered collection of numeric components called?",
    "Vector", "Database", "Function name", "Loop")

add("Linear Algebra", "Intermediate",
    "What is the dot product of perpendicular nonzero vectors?",
    "Zero", "One", "Infinity", "Always negative")

add("Linear Algebra", "Advanced",
    "What does a zero determinant imply for a square matrix?",
    "The matrix is singular",
    "The matrix is always diagonal",
    "Every element equals zero",
    "The matrix is always invertible")


# ==================================================
# MACHINE LEARNING
# ==================================================

add("Machine Learning", "Beginner",
    "Which learning method uses labelled examples?",
    "Supervised learning", "Unsupervised learning",
    "Random guessing", "Manual sorting")

add("Machine Learning", "Intermediate",
    "What is overfitting?",
    "Learning training-specific patterns that generalize poorly",
    "Having no training data",
    "Deleting the model",
    "Always predicting correctly")

add("Machine Learning", "Advanced",
    "Why is cross-validation used?",
    "To estimate generalization performance",
    "To guarantee perfect accuracy",
    "To remove every feature",
    "To avoid evaluating models")


# ==================================================
# NUMPY
# ==================================================

add("NumPy", "Beginner",
    "Which NumPy object stores multidimensional arrays?",
    "ndarray", "DataFrame", "HTML", "SQL table")

add("NumPy", "Intermediate",
    "What does reshape() change?",
    "Array dimensions while preserving element count",
    "Every element's numeric value",
    "The Python version",
    "The operating system")

add("NumPy", "Advanced",
    "What is broadcasting?",
    "Applying operations to compatible array shapes",
    "Sending emails",
    "Creating web pages",
    "Deleting duplicate files")


# ==================================================
# DEEP LEARNING
# ==================================================

add("Deep Learning", "Beginner",
    "What is a basic computational unit of a neural network?",
    "Artificial neuron", "SQL query", "HTML tag", "Git branch")

add("Deep Learning", "Intermediate",
    "Which activation function computes max(0, x)?",
    "ReLU", "Softmax", "Sigmoid", "Tanh")

add("Deep Learning", "Advanced",
    "Why is dropout used during training?",
    "To reduce overfitting",
    "To guarantee zero loss",
    "To remove the dataset",
    "To increase image resolution")


# ==================================================
# NETWORKING
# ==================================================

add("Networking", "Beginner",
    "What does DNS help resolve?",
    "Domain names to IP addresses",
    "Python variables", "CSS styles", "Excel formulas")

add("Networking", "Intermediate",
    "Which transport protocol provides reliable ordered delivery?",
    "TCP", "UDP", "ARP", "ICMP")

add("Networking", "Advanced",
    "What is a defensive benefit of network segmentation?",
    "Limiting the spread of security incidents",
    "Removing the need for authentication",
    "Guaranteeing unlimited bandwidth",
    "Disabling all monitoring")


# ==================================================
# LINUX
# ==================================================

add("Linux", "Beginner",
    "Which command displays the current directory?",
    "pwd", "echo", "date", "whoami")

add("Linux", "Intermediate",
    "Which command displays a snapshot of running processes?",
    "ps", "mkdir", "pwd", "clear")

add("Linux", "Advanced",
    "What is the principle of least privilege?",
    "Granting only the permissions needed for a task",
    "Giving everyone administrator access",
    "Removing all user accounts",
    "Sharing every password")


# ==================================================
# CYBERSECURITY FUNDAMENTALS
# ==================================================

add("Cybersecurity Fundamentals", "Beginner",
    "What does confidentiality protect?",
    "Information from unauthorized disclosure",
    "Screen brightness", "CPU temperature", "File size")

add("Cybersecurity Fundamentals", "Intermediate",
    "What is multi-factor authentication?",
    "Verification using multiple distinct factor types",
    "Using the same password twice",
    "Removing login requirements",
    "Sharing one account")

add("Cybersecurity Fundamentals", "Advanced",
    "What does defence in depth mean?",
    "Using multiple complementary security controls",
    "Depending on one password",
    "Disabling security updates",
    "Ignoring security alerts")


# ==================================================
# CRYPTOGRAPHY
# ==================================================

add("Cryptography", "Beginner",
    "What is the primary purpose of encryption?",
    "Protect data confidentiality",
    "Increase screen resolution",
    "Sort database records",
    "Delete duplicate files")

add("Cryptography", "Intermediate",
    "What distinguishes asymmetric encryption?",
    "It uses a public and private key pair",
    "It requires no keys",
    "It only works with images",
    "It always uses one shared key")

add("Cryptography", "Advanced",
    "What can a valid digital signature help verify?",
    "Authenticity and integrity",
    "Unlimited storage",
    "Network speed",
    "Screen brightness")


# ==================================================
# SECURITY MONITORING
# ==================================================

add("Security Monitoring", "Beginner",
    "What is a system log?",
    "A record of system events",
    "A computer screen",
    "A password manager",
    "A spreadsheet formula")

add("Security Monitoring", "Intermediate",
    "What is a false positive security alert?",
    "A harmless event incorrectly flagged as suspicious",
    "A confirmed incident",
    "A missing keyboard",
    "A software installation")

add("Security Monitoring", "Advanced",
    "Why correlate events from multiple log sources?",
    "To improve understanding of related security events",
    "To delete evidence",
    "To disable monitoring",
    "To replace every security control")


# ==================================================
# INCIDENT RESPONSE
# ==================================================

add("Incident Response", "Beginner",
    "What should an employee do after noticing a suspected security incident?",
    "Report it through the approved channel",
    "Ignore it",
    "Publish confidential information",
    "Delete all records")

add("Incident Response", "Intermediate",
    "What is the goal of incident containment?",
    "Limit the impact and spread of an incident",
    "Remove all documentation",
    "Increase the incident's impact",
    "Disable every backup")

add("Incident Response", "Advanced",
    "What is the purpose of a post-incident review?",
    "Identify lessons and improve future response",
    "Hide the incident",
    "Remove all security policies",
    "Avoid documenting improvements")
=======

"""PlaceReady adaptive assessment question bank."""

LEVELS = ("Beginner", "Intermediate", "Advanced")

QUESTION_BANK = []


def add(skill, level, question, correct, wrong1, wrong2, wrong3):
    QUESTION_BANK.append({
        "id": f"Q{len(QUESTION_BANK) + 1:03d}",
        "skill": skill,
        "level": level,
        "question": question,
        "options": [correct, wrong1, wrong2, wrong3],
        "answer": correct,
    })


# ==================================================
# PYTHON
# ==================================================

add("Python", "Beginner",
    "Which Python data type is mutable?",
    "List", "Tuple", "String", "Integer")

add("Python", "Intermediate",
    "What does a Python generator use to return values lazily?",
    "yield", "break", "continue", "import")

add("Python", "Advanced",
    "What is the main purpose of a context manager?",
    "Manage resource setup and cleanup",
    "Compile Python into Java",
    "Remove all exceptions",
    "Create global variables")


# ==================================================
# SQL
# ==================================================

add("SQL", "Beginner",
    "Which SQL keyword retrieves data?",
    "SELECT", "DELETE", "DROP", "UPDATE")

add("SQL", "Intermediate",
    "Which clause filters grouped results?",
    "HAVING", "WHERE", "ORDER BY", "LIMIT")

add("SQL", "Advanced",
    "Which window function assigns consecutive row numbers?",
    "ROW_NUMBER()", "SUM()", "COUNT()", "LOWER()")


# ==================================================
# DATA STRUCTURES
# ==================================================

add("Data Structures", "Beginner",
    "Which structure follows FIFO?",
    "Queue", "Stack", "Tree", "Set")

add("Data Structures", "Intermediate",
    "What is the time complexity of binary search on a sorted array?",
    "O(log n)", "O(n)", "O(n squared)", "O(2^n)")

add("Data Structures", "Advanced",
    "Which structure is commonly used to implement a priority queue?",
    "Heap", "Unsorted array only", "String", "Boolean")


# ==================================================
# GIT
# ==================================================

add("Git", "Beginner",
    "Which command displays the working tree status?",
    "git status", "git init", "git clone", "git push")

add("Git", "Intermediate",
    "Which command temporarily saves uncommitted changes?",
    "git stash", "git log", "git fetch", "git tag")

add("Git", "Advanced",
    "Which command finds the commit that introduced a bug using binary search?",
    "git bisect", "git status", "git remote", "git init")


# ==================================================
# HTML
# ==================================================

add("HTML", "Beginner",
    "Which HTML element creates a hyperlink?",
    "<a>", "<p>", "<div>", "<h1>")

add("HTML", "Intermediate",
    "Which attribute provides alternative text for an image?",
    "alt", "href", "class", "width")

add("HTML", "Advanced",
    "Which element represents a standalone piece of content?",
    "<article>", "<br>", "<span>", "<b>")


# ==================================================
# CSS
# ==================================================

add("CSS", "Beginner",
    "Which property changes text colour?",
    "color", "padding", "margin", "display")

add("CSS", "Intermediate",
    "Which layout system is designed for rows and columns together?",
    "CSS Grid", "Float only", "Text align", "Border radius")

add("CSS", "Advanced",
    "Which selector normally has the highest specificity?",
    "#header", ".header", "header", "*")


# ==================================================
# JAVASCRIPT
# ==================================================

add("JavaScript", "Beginner",
    "Which keyword declares a block-scoped variable that can be reassigned?",
    "let", "const", "def", "int")

add("JavaScript", "Intermediate",
    "Which method converts a JSON string into a JavaScript value?",
    "JSON.parse()", "JSON.stringify()", "JSON.create()", "JSON.read()")

add("JavaScript", "Advanced",
    "What does a closure allow a function to retain?",
    "Access to its lexical environment",
    "Access to every browser password",
    "Unlimited memory",
    "Automatic network access")


# ==================================================
# PROBLEM SOLVING
# ==================================================

add("Problem Solving", "Beginner",
    "What should you do first when solving a programming problem?",
    "Understand the requirements",
    "Write random code",
    "Ignore the inputs",
    "Delete the test cases")

add("Problem Solving", "Intermediate",
    "What does divide and conquer do?",
    "Splits a problem into smaller subproblems",
    "Removes all input",
    "Avoids using algorithms",
    "Always uses a database")

add("Problem Solving", "Advanced",
    "When is dynamic programming especially useful?",
    "When subproblems overlap and optimal substructure exists",
    "When no computation is needed",
    "Only when sorting strings",
    "Only when displaying HTML")


# ==================================================
# STATISTICS
# ==================================================

add("Statistics", "Beginner",
    "What is the mean of 2, 4 and 6?",
    "4", "2", "6", "12")

add("Statistics", "Intermediate",
    "Which measure describes how spread out values are?",
    "Standard deviation", "Mode", "Median", "Sample name")

add("Statistics", "Advanced",
    "What is a Type I error in hypothesis testing?",
    "Rejecting a true null hypothesis",
    "Failing to reject a false null hypothesis",
    "Calculating the mean",
    "Increasing the sample size")


# ==================================================
# EXCEL
# ==================================================

add("Excel", "Beginner",
    "Which function adds numbers?",
    "SUM", "COUNT", "MAX", "MIN")

add("Excel", "Intermediate",
    "Which feature summarizes large tables interactively?",
    "PivotTable", "Font colour", "Page margin", "Spell check")

add("Excel", "Advanced",
    "Which tool supports importing and transforming data?",
    "Power Query", "WordArt", "Page Break", "Print Preview")


# ==================================================
# PANDAS
# ==================================================

add("Pandas", "Beginner",
    "Which Pandas structure represents tabular data?",
    "DataFrame", "Integer", "Boolean", "Tuple only")

add("Pandas", "Intermediate",
    "Which method groups rows for aggregation?",
    "groupby()", "print()", "append()", "len()")

add("Pandas", "Advanced",
    "Which merge type preserves every row from the left table?",
    "Left join", "Inner join", "Right join", "Cross join")


# ==================================================
# DATA VISUALIZATION
# ==================================================

add("Data Visualization", "Beginner",
    "Which chart is suitable for comparing categories?",
    "Bar chart", "Paragraph", "Source code", "File tree")

add("Data Visualization", "Intermediate",
    "Which chart is useful for showing correlation between two numeric variables?",
    "Scatter plot", "Pie chart", "Single text label", "File icon")

add("Data Visualization", "Advanced",
    "Why should a standard bar chart generally start its value axis at zero?",
    "To avoid misleading comparisons of bar lengths",
    "To increase file size",
    "To remove category labels",
    "To change the underlying data")


# ==================================================
# LINEAR ALGEBRA
# ==================================================

add("Linear Algebra", "Beginner",
    "What is an ordered collection of numeric components called?",
    "Vector", "Database", "Function name", "Loop")

add("Linear Algebra", "Intermediate",
    "What is the dot product of perpendicular nonzero vectors?",
    "Zero", "One", "Infinity", "Always negative")

add("Linear Algebra", "Advanced",
    "What does a zero determinant imply for a square matrix?",
    "The matrix is singular",
    "The matrix is always diagonal",
    "Every element equals zero",
    "The matrix is always invertible")


# ==================================================
# MACHINE LEARNING
# ==================================================

add("Machine Learning", "Beginner",
    "Which learning method uses labelled examples?",
    "Supervised learning", "Unsupervised learning",
    "Random guessing", "Manual sorting")

add("Machine Learning", "Intermediate",
    "What is overfitting?",
    "Learning training-specific patterns that generalize poorly",
    "Having no training data",
    "Deleting the model",
    "Always predicting correctly")

add("Machine Learning", "Advanced",
    "Why is cross-validation used?",
    "To estimate generalization performance",
    "To guarantee perfect accuracy",
    "To remove every feature",
    "To avoid evaluating models")


# ==================================================
# NUMPY
# ==================================================

add("NumPy", "Beginner",
    "Which NumPy object stores multidimensional arrays?",
    "ndarray", "DataFrame", "HTML", "SQL table")

add("NumPy", "Intermediate",
    "What does reshape() change?",
    "Array dimensions while preserving element count",
    "Every element's numeric value",
    "The Python version",
    "The operating system")

add("NumPy", "Advanced",
    "What is broadcasting?",
    "Applying operations to compatible array shapes",
    "Sending emails",
    "Creating web pages",
    "Deleting duplicate files")


# ==================================================
# DEEP LEARNING
# ==================================================

add("Deep Learning", "Beginner",
    "What is a basic computational unit of a neural network?",
    "Artificial neuron", "SQL query", "HTML tag", "Git branch")

add("Deep Learning", "Intermediate",
    "Which activation function computes max(0, x)?",
    "ReLU", "Softmax", "Sigmoid", "Tanh")

add("Deep Learning", "Advanced",
    "Why is dropout used during training?",
    "To reduce overfitting",
    "To guarantee zero loss",
    "To remove the dataset",
    "To increase image resolution")


# ==================================================
# NETWORKING
# ==================================================

add("Networking", "Beginner",
    "What does DNS help resolve?",
    "Domain names to IP addresses",
    "Python variables", "CSS styles", "Excel formulas")

add("Networking", "Intermediate",
    "Which transport protocol provides reliable ordered delivery?",
    "TCP", "UDP", "ARP", "ICMP")

add("Networking", "Advanced",
    "What is a defensive benefit of network segmentation?",
    "Limiting the spread of security incidents",
    "Removing the need for authentication",
    "Guaranteeing unlimited bandwidth",
    "Disabling all monitoring")


# ==================================================
# LINUX
# ==================================================

add("Linux", "Beginner",
    "Which command displays the current directory?",
    "pwd", "echo", "date", "whoami")

add("Linux", "Intermediate",
    "Which command displays a snapshot of running processes?",
    "ps", "mkdir", "pwd", "clear")

add("Linux", "Advanced",
    "What is the principle of least privilege?",
    "Granting only the permissions needed for a task",
    "Giving everyone administrator access",
    "Removing all user accounts",
    "Sharing every password")


# ==================================================
# CYBERSECURITY FUNDAMENTALS
# ==================================================

add("Cybersecurity Fundamentals", "Beginner",
    "What does confidentiality protect?",
    "Information from unauthorized disclosure",
    "Screen brightness", "CPU temperature", "File size")

add("Cybersecurity Fundamentals", "Intermediate",
    "What is multi-factor authentication?",
    "Verification using multiple distinct factor types",
    "Using the same password twice",
    "Removing login requirements",
    "Sharing one account")

add("Cybersecurity Fundamentals", "Advanced",
    "What does defence in depth mean?",
    "Using multiple complementary security controls",
    "Depending on one password",
    "Disabling security updates",
    "Ignoring security alerts")


# ==================================================
# CRYPTOGRAPHY
# ==================================================

add("Cryptography", "Beginner",
    "What is the primary purpose of encryption?",
    "Protect data confidentiality",
    "Increase screen resolution",
    "Sort database records",
    "Delete duplicate files")

add("Cryptography", "Intermediate",
    "What distinguishes asymmetric encryption?",
    "It uses a public and private key pair",
    "It requires no keys",
    "It only works with images",
    "It always uses one shared key")

add("Cryptography", "Advanced",
    "What can a valid digital signature help verify?",
    "Authenticity and integrity",
    "Unlimited storage",
    "Network speed",
    "Screen brightness")


# ==================================================
# SECURITY MONITORING
# ==================================================

add("Security Monitoring", "Beginner",
    "What is a system log?",
    "A record of system events",
    "A computer screen",
    "A password manager",
    "A spreadsheet formula")

add("Security Monitoring", "Intermediate",
    "What is a false positive security alert?",
    "A harmless event incorrectly flagged as suspicious",
    "A confirmed incident",
    "A missing keyboard",
    "A software installation")

add("Security Monitoring", "Advanced",
    "Why correlate events from multiple log sources?",
    "To improve understanding of related security events",
    "To delete evidence",
    "To disable monitoring",
    "To replace every security control")


# ==================================================
# INCIDENT RESPONSE
# ==================================================

add("Incident Response", "Beginner",
    "What should an employee do after noticing a suspected security incident?",
    "Report it through the approved channel",
    "Ignore it",
    "Publish confidential information",
    "Delete all records")

add("Incident Response", "Intermediate",
    "What is the goal of incident containment?",
    "Limit the impact and spread of an incident",
    "Remove all documentation",
    "Increase the incident's impact",
    "Disable every backup")

add("Incident Response", "Advanced",
    "What is the purpose of a post-incident review?",
    "Identify lessons and improve future response",
    "Hide the incident",
    "Remove all security policies",
    "Avoid documenting improvements")
>>>>>>> c4b8fdf7f9c8cceb95af9e45525f2e45c3a95d65
