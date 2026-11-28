

"""Adaptive assessment and scoring engine for PlaceReady."""

import random

from gap_analysis.roles import JOB_ROLES

from gap_analysis.analyzer import (
    SKILL_SUGGESTIONS,
    DEFAULT_SUGGESTION,
)

from .questions import QUESTION_BANK, LEVELS


PASS_THRESHOLD = 80
QUESTIONS_PER_SKILL = 1


class AdaptiveAssessment:

    def __init__(self, role):

        if role not in JOB_ROLES:
            raise ValueError("Invalid career role.")

        self.role = role
        self.level_index = 0
        self.history = []
        self.completed = False

        self._questions = self._select_questions()


    @property
    def current_level(self):

        return LEVELS[self.level_index]


    def _select_questions(self):

        selected = []

        for skill in JOB_ROLES[self.role]:

            available = [
                question
                for question in QUESTION_BANK
                if question["skill"] == skill
                and question["level"] == self.current_level
            ]

            if not available:
                raise ValueError(
                    f"No {self.current_level} questions "
                    f"available for {skill}."
                )

            count = min(
                QUESTIONS_PER_SKILL,
                len(available)
            )

            for original in random.sample(available, count):

                question = {
                    **original,
                    "options": list(original["options"]),
                }

                random.shuffle(question["options"])

                selected.append(question)

        random.shuffle(selected)

        return selected


    def get_questions(self):
        """Return questions without revealing correct answers."""

        if self.completed:
            return []

        return [
            {
                "id": question["id"],
                "skill": question["skill"],
                "level": question["level"],
                "question": question["question"],
                "options": list(question["options"]),
            }
            for question in self._questions
        ]


    def submit_answers(self, answers):
        """Accept a dictionary of question IDs and selected options."""

        if self.completed:
            raise ValueError("Assessment is already completed.")

        if not isinstance(answers, dict):
            raise ValueError("Answers must be a dictionary.")

        expected_ids = {
            question["id"]
            for question in self._questions
        }

        if set(answers) != expected_ids:
            raise ValueError(
                "Submit exactly one answer for every question."
            )

        correct_count = 0
        skill_results = {}

        for question in self._questions:

            selected = answers[question["id"]]

            if selected not in question["options"]:
                raise ValueError(
                    f"Invalid answer for {question['id']}."
                )

            skill = question["skill"]

            if skill not in skill_results:
                skill_results[skill] = {
                    "correct": 0,
                    "total": 0,
                }

            skill_results[skill]["total"] += 1

            if selected == question["answer"]:

                correct_count += 1
                skill_results[skill]["correct"] += 1

        total = len(self._questions)

        score = round(
            correct_count / total * 100,
            2
        )

        passed = (
            correct_count * 100
            >= total * PASS_THRESHOLD
        )

        result = {
            "level": self.current_level,
            "correct": correct_count,
            "total": total,
            "score": score,
            "passed": passed,
            "skill_results": skill_results,
        }

        self.history.append(result)

        if passed and self.level_index < len(LEVELS) - 1:

            self.level_index += 1

            self._questions = self._select_questions()

        else:

            self.completed = True
            self._questions = []

        return {
            "result": result,
            "completed": self.completed,
            "next_level": (
                None
                if self.completed
                else self.current_level
            ),
        }


    def generate_report(self):
        """Generate the final assessment report."""

        if not self.completed:
            raise ValueError(
                "Complete the assessment before generating a report."
            )

        total_correct = 0
        total_questions = 0

        estimated_level = "Foundation practice recommended"

        combined_skills = {}

        for stage in self.history:

            total_correct += stage["correct"]
            total_questions += stage["total"]

            if stage["passed"]:
                estimated_level = stage["level"]

            for skill, data in stage["skill_results"].items():

                if skill not in combined_skills:
                    combined_skills[skill] = {
                        "correct": 0,
                        "total": 0,
                    }

                combined_skills[skill]["correct"] += data["correct"]

                combined_skills[skill]["total"] += data["total"]

        skill_scores = {}

        for skill, data in combined_skills.items():

            skill_scores[skill] = round(
                data["correct"] / data["total"] * 100,
                2
            )

        weak_skills = sorted(
            [
                skill
                for skill, score in skill_scores.items()
                if score < PASS_THRESHOLD
            ],
            key=lambda skill: skill_scores[skill]
        )

        strengths = [
            skill
            for skill, score in skill_scores.items()
            if score >= PASS_THRESHOLD
        ]

        recommendations = []

        for skill in weak_skills:

            score = skill_scores[skill]

            if score < 40:
                priority = "High"

            elif score < 60:
                priority = "Medium"

            else:
                priority = "Low"

            suggestion = SKILL_SUGGESTIONS.get(
                skill, {}
            ).get(
                priority,
                DEFAULT_SUGGESTION
            )

            recommendations.append({
                "skill": skill,
                "score": score,
                "priority": priority,
                "suggestion": suggestion,
            })

        overall_score = round(
            total_correct / total_questions * 100,
            2
        )

        return {
            "target_role": self.role,
            "overall_score": overall_score,
            "estimated_level": estimated_level,
            "total_correct": total_correct,
            "total_questions": total_questions,
            "skill_scores": skill_scores,
            "strengths": strengths,
            "weak_skills": weak_skills,
            "recommendations": recommendations,
            "history": self.history,
=======

"""Adaptive assessment and scoring engine for PlaceReady."""

import random

from gap_analysis.roles import JOB_ROLES

from gap_analysis.analyzer import (
    SKILL_SUGGESTIONS,
    DEFAULT_SUGGESTION,
)

from .questions import QUESTION_BANK, LEVELS


PASS_THRESHOLD = 80
QUESTIONS_PER_SKILL = 1


class AdaptiveAssessment:

    def __init__(self, role):

        if role not in JOB_ROLES:
            raise ValueError("Invalid career role.")

        self.role = role
        self.level_index = 0
        self.history = []
        self.completed = False

        self._questions = self._select_questions()


    @property
    def current_level(self):

        return LEVELS[self.level_index]


    def _select_questions(self):

        selected = []

        for skill in JOB_ROLES[self.role]:

            available = [
                question
                for question in QUESTION_BANK
                if question["skill"] == skill
                and question["level"] == self.current_level
            ]

            if not available:
                raise ValueError(
                    f"No {self.current_level} questions "
                    f"available for {skill}."
                )

            count = min(
                QUESTIONS_PER_SKILL,
                len(available)
            )

            for original in random.sample(available, count):

                question = {
                    **original,
                    "options": list(original["options"]),
                }

                random.shuffle(question["options"])

                selected.append(question)

        random.shuffle(selected)

        return selected


    def get_questions(self):
        """Return questions without revealing correct answers."""

        if self.completed:
            return []

        return [
            {
                "id": question["id"],
                "skill": question["skill"],
                "level": question["level"],
                "question": question["question"],
                "options": list(question["options"]),
            }
            for question in self._questions
        ]


    def submit_answers(self, answers):
        """Accept a dictionary of question IDs and selected options."""

        if self.completed:
            raise ValueError("Assessment is already completed.")

        if not isinstance(answers, dict):
            raise ValueError("Answers must be a dictionary.")

        expected_ids = {
            question["id"]
            for question in self._questions
        }

        if set(answers) != expected_ids:
            raise ValueError(
                "Submit exactly one answer for every question."
            )

        correct_count = 0
        skill_results = {}

        for question in self._questions:

            selected = answers[question["id"]]

            if selected not in question["options"]:
                raise ValueError(
                    f"Invalid answer for {question['id']}."
                )

            skill = question["skill"]

            if skill not in skill_results:
                skill_results[skill] = {
                    "correct": 0,
                    "total": 0,
                }

            skill_results[skill]["total"] += 1

            if selected == question["answer"]:

                correct_count += 1
                skill_results[skill]["correct"] += 1

        total = len(self._questions)

        score = round(
            correct_count / total * 100,
            2
        )

        passed = (
            correct_count * 100
            >= total * PASS_THRESHOLD
        )

        result = {
            "level": self.current_level,
            "correct": correct_count,
            "total": total,
            "score": score,
            "passed": passed,
            "skill_results": skill_results,
        }

        self.history.append(result)

        if passed and self.level_index < len(LEVELS) - 1:

            self.level_index += 1

            self._questions = self._select_questions()

        else:

            self.completed = True
            self._questions = []

        return {
            "result": result,
            "completed": self.completed,
            "next_level": (
                None
                if self.completed
                else self.current_level
            ),
        }


    def generate_report(self):
        """Generate the final assessment report."""

        if not self.completed:
            raise ValueError(
                "Complete the assessment before generating a report."
            )

        total_correct = 0
        total_questions = 0

        estimated_level = "Foundation practice recommended"

        combined_skills = {}

        for stage in self.history:

            total_correct += stage["correct"]
            total_questions += stage["total"]

            if stage["passed"]:
                estimated_level = stage["level"]

            for skill, data in stage["skill_results"].items():

                if skill not in combined_skills:
                    combined_skills[skill] = {
                        "correct": 0,
                        "total": 0,
                    }

                combined_skills[skill]["correct"] += data["correct"]

                combined_skills[skill]["total"] += data["total"]

        skill_scores = {}

        for skill, data in combined_skills.items():

            skill_scores[skill] = round(
                data["correct"] / data["total"] * 100,
                2
            )

        weak_skills = sorted(
            [
                skill
                for skill, score in skill_scores.items()
                if score < PASS_THRESHOLD
            ],
            key=lambda skill: skill_scores[skill]
        )

        strengths = [
            skill
            for skill, score in skill_scores.items()
            if score >= PASS_THRESHOLD
        ]

        recommendations = []

        for skill in weak_skills:

            score = skill_scores[skill]

            if score < 40:
                priority = "High"

            elif score < 60:
                priority = "Medium"

            else:
                priority = "Low"

            suggestion = SKILL_SUGGESTIONS.get(
                skill, {}
            ).get(
                priority,
                DEFAULT_SUGGESTION
            )

            recommendations.append({
                "skill": skill,
                "score": score,
                "priority": priority,
                "suggestion": suggestion,
            })

        overall_score = round(
            total_correct / total_questions * 100,
            2
        )

        return {
            "target_role": self.role,
            "overall_score": overall_score,
            "estimated_level": estimated_level,
            "total_correct": total_correct,
            "total_questions": total_questions,
            "skill_scores": skill_scores,
            "strengths": strengths,
            "weak_skills": weak_skills,
            "recommendations": recommendations,
            "history": self.history,
>>>>>>> c4b8fdf7f9c8cceb95af9e45525f2e45c3a95d65
        }