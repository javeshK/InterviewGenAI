from database.db import db
from models.interview_question import InterviewQuestion


class InterviewQuestionRepository:

    @staticmethod
    def add(question: InterviewQuestion):
        db.session.add(question)

    @staticmethod
    def get(question_id: str):
        return InterviewQuestion.query.get(question_id)

    @staticmethod
    def get_by_interview(interview_id: str):

        return (
            InterviewQuestion.query
            .filter_by(interview_id=interview_id)
            .order_by(
                InterviewQuestion.question_number
            )
            .all()
        )

    @staticmethod
    def get_by_number(
        interview_id: str,
        question_number: int
    ):

        return (
            InterviewQuestion.query
            .filter_by(
                interview_id=interview_id,
                question_number=question_number
            )
            .first()
        )

    @staticmethod
    def get_latest(interview_id: str):

        return (
            InterviewQuestion.query
            .filter_by(interview_id=interview_id)
            .order_by(
                InterviewQuestion.question_number.desc()
            )
            .first()
        )

    @staticmethod
    def delete(question: InterviewQuestion):
        db.session.delete(question)