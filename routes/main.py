from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from services.interview_service import InterviewService
from services.session_manager import SessionManager

main = Blueprint("main", __name__)

# Create one instance of InterviewService
interview_service = InterviewService()


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/setup", methods=["GET", "POST"])
def setup():

    if request.method == "POST":

        name = request.form["name"]

        # Optional email field
        email = request.form.get("email")

        role = request.form["role"]

        experience = request.form["experience"]

        interview_type = request.form["interview_type"]

        difficulty = request.form["difficulty"]

        try:

            interview_session = interview_service.start_interview(

                name=name,

                email=email,

                role=role,

                experience=experience,

                interview_type=interview_type,

                difficulty=difficulty
            )

            return redirect(
                url_for(
                    "main.interview",
                    interview_id=interview_session.interview_id
                )
            )

        except Exception as e:

            print(e)

            return render_template(
                "setup.html",
                error="Failed to start interview. Please try again."
            )

    return render_template("setup.html")


@main.route("/interview/<int:interview_id>")
def interview(interview_id):

    interview_session = SessionManager.get_session(interview_id)

    if interview_session is None:
        return "Interview session not found.", 404

    return render_template(
        "interview.html",
        session=interview_session
    )