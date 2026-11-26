
from .analyzer import get_recommendations


def generate_roadmap(analysis_result, weeks=4):
    """Generate a preparation roadmap based on skill gaps."""

    if not isinstance(analysis_result, dict):
        return []

    if not analysis_result.get("success"):
        return []

    if type(weeks) is not int or not 2 <= weeks <= 12:
        raise ValueError(
            "Preparation duration must be between 2 and 12 weeks."
        )

    recommendations = get_recommendations(
        analysis_result
    )

    weak_skills = [
        item for item in recommendations
        if item["gap"] > 0
    ]

    roadmap = []

    # Reserve the final week for reassessment
    learning_weeks = weeks - 1

    # Handle students who have no skill gaps
    if not weak_skills:

        for week in range(1, weeks):
            roadmap.append({
                "week": week,
                "title": "Maintain your skills",
                "activities": [{
                    "skill": "Revision",
                    "priority": "None",
                    "topics": [
                        "Revise existing concepts",
                        "Practice interview questions"
                    ],
                    "task": "Complete a practice project."
                }]
            })

    else:

        # Create weekly learning groups
        groups = [
            [] for _ in range(learning_weeks)
        ]

        # Distribute every weak skill across the weeks
        total_skills = len(weak_skills)

        for index, item in enumerate(weak_skills):

            if total_skills >= learning_weeks:
                week_index = (
                    index * learning_weeks // total_skills
                )
            else:
                week_index = index

            groups[week_index].append({
                "skill": item["skill"],
                "priority": item["priority"],
                "gap": item["gap"],
                "topics": item["topics"],
                "task": item["task"],
                "suggestion": item["suggestion"]
            })

        # Generate the weekly roadmap
        for index, activities in enumerate(groups):

            if activities:

                title = " and ".join(
                    activity["skill"]
                    for activity in activities
                )

            else:

                title = "Practice and revision"

                activities = [{
                    "skill": "Revision",
                    "priority": "None",
                    "topics": [
                        "Review previously studied topics",
                        "Practice technical questions"
                    ],
                    "task": "Complete a mini project."
                }]

            roadmap.append({
                "week": index + 1,
                "title": title,
                "activities": activities
            })

    # Final week
    roadmap.append({
        "week": weeks,
        "title": "Final revision and reassessment",
        "activities": [{
            "skill": "Assessment",
            "priority": "Review",
            "topics": [
                "Revise important concepts",
                "Review previous mistakes",
                "Practice interview questions"
            ],
            "task": (
                "Retake the skill assessment "
                "and compare your readiness score."
            )
        }]
    })

    return roadmap
