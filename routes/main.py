from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/setup", methods=["GET", "POST"])
def setup():

    if request.method == "POST":

        name = request.form["name"]
        role = request.form["role"]
        experience = request.form["experience"]
        interview_type = request.form["interview_type"]
        difficulty = request.form["difficulty"]

        # Save in session
        session["name"] = name
        session["role"] = role
        session["experience"] = experience
        session["interview_type"] = interview_type
        session["difficulty"] = difficulty

        return redirect(url_for("main.interview"))

    return render_template("setup.html")

@main.route("/interview")
def interview():

    interview_data = {
        "name": session.get("name"),
        "role": session.get("role"),
        "experience": session.get("experience"),
        "interview_type": session.get("interview_type"),
        "difficulty": session.get("difficulty")
    }

    return render_template(
        "interview.html",
        interview=interview_data
    )