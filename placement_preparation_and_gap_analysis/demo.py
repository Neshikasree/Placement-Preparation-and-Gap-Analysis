
"""Standalone demo for Member 1's module (no database or Flask needed).

Run from the project root:   python demo.py
"""

from gap_analysis import analyze_skills, get_recommendations
from gap_analysis.roles import JOB_ROLES, SKILL_LEVEL_LABELS


def print_report(result):
    if not result["success"]:
        print("\nCould not analyse:")
        for error in result["errors"]:
            print("  -", error)
        return

    print("\n" + "=" * 60)
    print("Target role     :", result["target_role"])
    print("Readiness score : {}%".format(result["readiness_score"]))
    print("Points          : {} / {}".format(result["total_achieved_points"],
                                             result["total_required_points"]))
    print("=" * 60)
    print("{:<18}{:>9}{:>9}{:>6}".format("Skill", "Required", "Current", "Gap"))
    for item in result["skill_gaps"]:
        note = "  (not provided)" if item["missing"] else ""
        print("{:<18}{:>9}{:>9}{:>6}{}".format(
            item["skill"], item["required_level"], item["current_level"], item["gap"], note))

    print("\nRecommendations (biggest gap first):")
    for rec in get_recommendations(result):
        print("\n  [{}] {} (gap {})".format(rec["priority"], rec["skill"], rec["gap"]))
        print("     ", rec["advice"])
        print("     ", rec["suggestion"])


def run_sample():
    print("\n--- Sample student: Python Developer ---")
    skills = {"Python": 3, "SQL": 2, "Data Structures": 4}  # Git missing on purpose
    print_report(analyze_skills("Python Developer", skills))

    print("\n--- Sample: invalid role ---")
    print_report(analyze_skills("Chef", skills))

    print("\n--- Sample: invalid rating ---")
    print_report(analyze_skills("Python Developer", {"Python": 9}))


def run_interactive():
    roles = list(JOB_ROLES)
    print("\nChoose a target role:")
    for number, name in enumerate(roles, start=1):
        print("  {}. {}".format(number, name))
    choice = input("Enter 1-{}: ".format(len(roles))).strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(roles):
        print("Invalid choice.")
        return
    role = roles[int(choice) - 1]

    print("\nRating scale:", ", ".join("{}={}".format(k, v) for k, v in SKILL_LEVEL_LABELS.items()))
    print("Press Enter to skip a skill (counts as 0).")
    skills = {}
    for skill in JOB_ROLES[role]:
        value = input("Your {} level (0-5): ".format(skill)).strip()
        if value:
            skills[skill] = value  # analyze_skills validates it
    print_report(analyze_skills(role, skills))


def main():
    while True:
        print("\n1. Run sample data\n2. Enter my own skills\n3. Exit")
        option = input("Choose: ").strip()
        if option == "1":
            run_sample()
        elif option == "2":
            run_interactive()
        elif option == "3":
            break
        else:
            print("Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
