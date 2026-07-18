from database.db import db
from models.interview import Interview


class InterviewRepository:

    @staticmethod
    def create(candidate_id,
               role,
               experience,
               interview_type,
               difficulty):

        interview = Interview(

            candidate_id=candidate_id,

            role=role,

            experience=experience,

            interview_type=interview_type,

            difficulty=difficulty
        )

        db.session.add(interview)
        db.session.flush()

        return interview

    @staticmethod
    def get(interview_id):

        return Interview.query.get(interview_id)

    @staticmethod
    def save():

        db.session.commit()