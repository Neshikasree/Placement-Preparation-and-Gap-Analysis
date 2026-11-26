
def calculate_quiz_history(attempts):
    """Calculate performance statistics for comparable quizzes.

    Attempts must belong to the same student,
    career role and difficulty level.
    """

    if not attempts:

        return {
            "total_attempts": 0,
            "highest_score": 0,
            "lowest_score": 0,
            "average_score": 0,
            "latest_score": 0,
            "improvement": 0,
            "history": []
        }

    # Sort from oldest attempt to newest
    attempts = sorted(
        attempts,
        key=lambda item: (
            item["created_at"],
            item["id"]
        )
    )

    roles = {
        item["target_role"] for item in attempts
    }

    levels = {
        item["level"] for item in attempts
    }

    if len(roles) != 1 or len(levels) != 1:
        raise ValueError(
            "Compare attempts from the same role and level."
        )

    scores = [
        float(item["score"])
        for item in attempts
    ]

    total_attempts = len(scores)

    highest_score = max(scores)
    lowest_score = min(scores)

    average_score = round(
        sum(scores) / total_attempts,
        2
    )

    latest_score = scores[-1]
    first_score = scores[0]

    improvement = round(
        latest_score - first_score,
        2
    )

    history = []

    for index, attempt in enumerate(attempts):

        history.append({
            "attempt": index + 1,
            "target_role": attempt["target_role"],
            "level": attempt["level"],
            "score": attempt["score"],
            "date": attempt["created_at"]
        })

    return {
        "total_attempts": total_attempts,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "average_score": average_score,
        "latest_score": latest_score,
        "improvement": improvement,
        "history": history
    }
