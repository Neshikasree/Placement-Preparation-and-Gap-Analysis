

"""PlaceReady adaptive assessment demo."""

from gap_analysis.roles import JOB_ROLES
from adaptive_assessment import AdaptiveAssessment


def main():

    print("=" * 50)
    print("WELCOME TO PLACEREADY")
    print("Adaptive Career Skill Assessment")
    print("=" * 50)

    roles = list(JOB_ROLES)

    for i, role in enumerate(roles, start=1):
        print(f"{i}. {role}")

    while True:
        choice = input("\nSelect your career: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(roles):
            break

        print("Invalid choice. Try again.")

    role = roles[int(choice) - 1]

    assessment = AdaptiveAssessment(role)

    while not assessment.completed:

        print("\n" + "=" * 50)
        print(assessment.current_level.upper(), "ASSESSMENT")
        print("=" * 50)

        questions = assessment.get_questions()
        answers = {}

        for i, question in enumerate(questions, start=1):

            print(f"\nQuestion {i}/{len(questions)}")
            print("Skill:", question["skill"])
            print(question["question"])

            for j, option in enumerate(
                question["options"], start=1
            ):
                print(f"{j}. {option}")

            while True:

                choice = input("Your answer: ").strip()

                if choice in {"1", "2", "3", "4"}:

                    answers[question["id"]] = (
                        question["options"][int(choice) - 1]
                    )

                    break

                print("Enter a number from 1 to 4.")

        response = assessment.submit_answers(answers)

        result = response["result"]

        print("\nScore:", result["score"], "%")

        if result["passed"]:
            print("Level passed!")
        else:
            print("More practice recommended.")

        if response["next_level"]:
            print("Next level:", response["next_level"])

    report = assessment.generate_report()

    print("\n" + "=" * 50)
    print("PLACEREADY - FINAL REPORT")
    print("=" * 50)

    print("Career:", report["target_role"])
    print("Overall score:", report["overall_score"], "%")
    print("Estimated level:", report["estimated_level"])

    print("\nSkill-wise scores:")

    for skill, score in report["skill_scores"].items():
        print(f"{skill}: {score}%")

    print("\nStrengths:")

    for skill in report["strengths"]:
        print("-", skill)

    print("\nSkills to improve:")

    for skill in report["weak_skills"]:
        print("-", skill)

    print("\nRecommendations:")

    for item in report["recommendations"]:
        print(f"\n{item['skill']} - {item['priority']}")
        print(item["suggestion"])

    print("\nAssessment completed!")
    print("Note: This is a preliminary knowledge estimate.")


if __name__ == "__main__":
    main()
