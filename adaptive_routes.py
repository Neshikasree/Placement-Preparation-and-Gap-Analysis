
import sys
import secrets
import time
from pathlib import Path
from threading import RLock

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
)

# Support the existing folder structure
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "placement-gap-analysis"))

from gap_analysis.roles import JOB_ROLES
from adaptive_assessment import AdaptiveAssessment


adaptive_bp = Blueprint(
    "adaptive",
    __name__,
    url_prefix="/adaptive"
)

attempts = {}
lock = RLock()

ATTEMPT_LIFETIME = 3600
MAX_ATTEMPTS = 500


# Security token
def csrf_token():
    if "adaptive_csrf" not in session:
        session["adaptive_csrf"] = secrets.token_hex(32)

    return session["adaptive_csrf"]


def verify_csrf():
    expected = session.get("adaptive_csrf", "")
    received = request.form.get("csrf_token", "")

    if not expected or not secrets.compare_digest(
        expected, received
    ):
        abort(400, "Invalid security token.")


# Remove expired attempts
def cleanup_attempts():
    now = time.monotonic()

    expired = [
        key for key, data in attempts.items()
        if now - data["updated"] > ATTEMPT_LIFETIME
    ]

    for key in expired:
        attempts.pop(key, None)


def current_attempt():
    cleanup_attempts()

    attempt_id = session.get("adaptive_attempt_id")
    data = attempts.get(attempt_id)

    if data:
        data["updated"] = time.monotonic()

    return data


# Career selection page
@adaptive_bp.route("/", methods=["GET", "POST"])
def start():

    if request.method == "POST":

        verify_csrf()

        role = request.form.get("role")

        if role not in JOB_ROLES:
            return render_template(
                "adaptive_start.html",
                roles=JOB_ROLES,
                csrf_token=csrf_token(),
                error="Please select a valid career."
            ), 400

        with lock:

            cleanup_attempts()

            old_id = session.get("adaptive_attempt_id")
            attempts.pop(old_id, None)

            if len(attempts) >= MAX_ATTEMPTS:
                abort(503, "Please try again later.")

            attempt_id = secrets.token_hex(32)

            attempts[attempt_id] = {
                "assessment": AdaptiveAssessment(role),
                "token": secrets.token_hex(32),
                "updated": time.monotonic()
            }

            session["adaptive_attempt_id"] = attempt_id

        return redirect(url_for("adaptive.quiz"))

    return render_template(
        "adaptive_start.html",
        roles=JOB_ROLES,
        csrf_token=csrf_token()
    )


# Adaptive quiz page
@adaptive_bp.route("/quiz", methods=["GET", "POST"])
def quiz():

    with lock:

        data = current_attempt()

        if data is None:
            return redirect(url_for("adaptive.start"))

        assessment = data["assessment"]

        if assessment.completed:
            return redirect(url_for("adaptive.results"))

        error = None

        if request.method == "POST":

            verify_csrf()

            submitted_token = request.form.get(
                "attempt_token", ""
            )

            if not secrets.compare_digest(
                submitted_token, data["token"]
            ):
                abort(400, "Expired assessment form.")

            answers = {}

            for question in assessment.get_questions():

                field = f"q_{question['id']}"
                values = request.form.getlist(field)

                if len(values) == 1:
                    answers[question["id"]] = values[0]

            try:

                assessment.submit_answers(answers)

                data["token"] = secrets.token_hex(32)

                if assessment.completed:
                    return redirect(
                        url_for("adaptive.results")
                    )

                return redirect(url_for("adaptive.quiz"))

            except ValueError as exc:
                error = str(exc)

        return render_template(
            "adaptive_quiz.html",
            role=assessment.role,
            level=assessment.current_level,
            questions=assessment.get_questions(),
            csrf_token=csrf_token(),
            attempt_token=data["token"],
            error=error
        )


# Final assessment report
@adaptive_bp.route("/results")
def results():

    with lock:

        data = current_attempt()

        if data is None:
            return redirect(url_for("adaptive.start"))

        assessment = data["assessment"]

        if not assessment.completed:
            return redirect(url_for("adaptive.quiz"))

        report = assessment.generate_report()

        return render_template(
            "adaptive_results.html",
            report=report
        )
