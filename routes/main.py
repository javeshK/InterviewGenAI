"""
routes/main.py

Main application routes.

Responsibilities
----------------
- Home page
- Interview setup
- Interview page
- Submit answer API
"""

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from dto.interview_request import InterviewRequest
from services.interview_service import InterviewService

main = Blueprint("main", __name__)

interview_service = InterviewService()


# ==========================================================
# Home
# ==========================================================

@main.route("/")
def home():
    return render_template("index.html")


# ==========================================================
# Interview Setup
# ==========================================================

@main.route("/setup", methods=["GET", "POST"])
def setup():

    if request.method == "GET":
        return render_template("setup.html")

    try:

        interview_request = InterviewRequest(

            full_name=request.form["name"],

            email=request.form.get("email", "").strip(),

            target_role=request.form["role"],

            experience=request.form["experience"],

            interview_type=request.form["interview_type"],

            difficulty=request.form["difficulty"],

            total_questions=10,

        )

        interview = interview_service.start_interview(
            interview_request
        )

        return redirect(
            url_for(
                "main.interview",
                interview_id=interview.id,
            )
        )

    except Exception as e:

        print(e)

        return render_template(
            "setup.html",
            error="Unable to start interview.",
        )


# ==========================================================
# Interview Screen
# ==========================================================

@main.route("/interview/<interview_id>")
def interview(interview_id):

    interview = interview_service.get_interview(
        interview_id
    )

    if interview is None:

        return (
            "Interview not found.",
            404,
        )

    current_question = (
        interview_service.get_current_question(
            interview_id
        )
    )

    return render_template(

        "interview.html",

        interview=interview,

        question=current_question,

    )


# ==========================================================
# Submit Answer
# ==========================================================

@main.route("/submit-answer", methods=["POST"])
def submit_answer():

    try:

        data = request.get_json()

        interview_id = data["interview_id"]

        answer = data["answer"]

        result = (
            interview_service.submit_answer(
                interview_id,
                answer,
            )
        )

        if result["completed"]:

            return jsonify(

                {
                    "completed": True,

                    "redirect": url_for(
                        "main.report",
                        interview_id=interview_id,
                    ),
                }

            )

        question = result["question"]

        return jsonify(

            {

                        "completed": False,

                        "question":
                            question.question,

                        "question_number":
                            question.question_number,

                        "feedback":
                            result["feedback"],

                        "technical_score":
                            result["technical_score"],

                        "communication_score":
                            result["communication_score"],

                        "confidence_score":
                            result["confidence_score"],

                        "overall_score":
                            result["overall_score"],

            }

        )

    except Exception as e:

        print(e)

        return (

            jsonify(

                {

                    "error": str(e)

                }

            ),

            500,

        )


# ==========================================================
# Interview Report
# ==========================================================

@main.route("/report/<interview_id>")
def report(interview_id):

    interview = interview_service.get_interview(
        interview_id
    )

    if interview is None:

        return (
            "Interview not found.",
            404,
        )

    return render_template(

        "report.html",

        interview=interview,

    )