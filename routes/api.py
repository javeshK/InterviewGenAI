from flask import Blueprint
from flask import request
from flask import jsonify

from services.interview_service import InterviewService

api = Blueprint("api", __name__)

interview_service = InterviewService()


@api.route("/answer", methods=["POST"])
def answer():

    data = request.get_json()

    answer = data.get("answer")

    session_id = data.get("session_id")

    result = interview_service.process_answer(
        session_id,
        answer
    )

    return jsonify(result)