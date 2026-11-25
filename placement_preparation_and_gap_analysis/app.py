"""Flask web application (Member 3): routes, pages and integration.

Run from the project root:   python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from resources import RESOURCES
from database import (get_results, get_student, get_student_skills, init_db,
                      list_students, save_assessment, save_result, add_student)
from gap_analysis import analyze_skills, get_recommendations
from gap_analysis.roles import JOB_ROLES, SKILL_LEVEL_LABELS


def readiness_level(score):
    """Turn a 0-100 score into a label and a CSS class for the dashboard."""
    if score >= 80:
        return "Placement ready", "excellent"
    if score >= 60:
        return "Almost ready", "good"
    if score >= 40:
        return "Making progress", "fair"
    return "Just getting started", "low"


def create_app(db_path=None):
    """Build the Flask app. db_path lets the tests use a temporary database."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
    app.config["DB_PATH"] = db_path
    init_db(db_path)  # creates placement.db and the tables if they do not exist

    def db():
        return app.config["DB_PATH"]

    # ------------------------------------------------------------------
    # Home / registration
    # ------------------------------------------------------------------
    @app.route("/")
    def index():
        return render_template("index.html", roles=list(JOB_ROLES), form={})

    @app.route("/register", methods=["POST"])
    def register():
        try:
            student_id = add_student(
                request.form.get("name"),
                request.form.get("email"),
                request.form.get("target_role"),
                db_path=db(),
            )
        except ValueError as error:
            flash(str(error), "error")
            return render_template("index.html", roles=list(JOB_ROLES), form=request.form), 400
        flash("Registration successful! Now rate your current skills.", "success")
        return redirect(url_for("assessment", student_id=student_id))

    # ------------------------------------------------------------------
    # Skill assessment
    # ------------------------------------------------------------------
    @app.route("/assessment/<int:student_id>", methods=["GET", "POST"])
    def assessment(student_id):
        student = get_student(student_id, db_path=db())
        if student is None:
            abort(404)
        required_skills = JOB_ROLES[student["target_role"]]

        if request.method == "POST":
            ratings = {}
            for skill in required_skills:
                value = request.form.get(skill, "").strip()
                if value != "":
                    ratings[skill] = value
            try:
                save_assessment(student_id, ratings, db_path=db())
            except ValueError as error:
                flash(str(error), "error")
                return render_template("assessment.html", student=student, skills=required_skills,
                                       levels=SKILL_LEVEL_LABELS, current=ratings), 400

            # Member 1's module does the calculation; Member 2 stores the score.
            result = analyze_skills(student["target_role"], get_student_skills(student_id, db_path=db()))
            if result["success"]:
                save_result(student_id, student["target_role"], result["readiness_score"], db_path=db())
            return redirect(url_for("results", student_id=student_id))

        return render_template("assessment.html", student=student, skills=required_skills,
                               levels=SKILL_LEVEL_LABELS,
                               current=get_student_skills(student_id, db_path=db()))

    # ------------------------------------------------------------------
    # Results dashboard
    # ------------------------------------------------------------------
    @app.route("/results/<int:student_id>")
    def results(student_id):
        student = get_student(student_id, db_path=db())
        if student is None:
            abort(404)

        skills = get_student_skills(student_id, db_path=db())
        if not skills:
            flash("Please complete your skill assessment first.", "error")
            return redirect(url_for("assessment", student_id=student_id))

        result = analyze_skills(student["target_role"], skills)
        if not result["success"]:
            for message in result["errors"]:
                flash(message, "error")
            return redirect(url_for("assessment", student_id=student_id))

        level_label, level_class = readiness_level(result["readiness_score"])
        return render_template(
            "results.html",
            student=student,
            result=result,
            resources=RESOURCES,
            recommendations=get_recommendations(result),
            history=get_results(student_id, db_path=db()),
            level_label=level_label,
            level_class=level_class,
            max_level=5,
        )

    # ------------------------------------------------------------------
    # Student list
    # ------------------------------------------------------------------
    @app.route("/students")
    def students():
        rows = []
        for student in list_students(db_path=db()):
            history = get_results(student["id"], db_path=db())
            rows.append({"student": student, "latest": history[0] if history else None})
        return render_template("students.html", rows=rows)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
