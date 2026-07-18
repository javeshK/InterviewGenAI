from database.db import db
from models.interview import Interview


class InterviewRepository:

    @staticmethod
    def add(interview: Interview):
        db.session.add(interview)

    @staticmethod
    def get(interview_id: str):
        return Interview.query.get(interview_id)

    @staticmethod
    def get_all():
        return Interview.query.all()

    @staticmethod
    def get_active(candidate_id: str):

        return (
            Interview.query
            .filter_by(
                candidate_id=candidate_id,
                status="In Progress"
            )
            .first()
        )

    @staticmethod
    def delete(interview: Interview):
        db.session.delete(interview)