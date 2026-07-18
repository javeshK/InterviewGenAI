from database.db import db
from models.candidate import Candidate


class CandidateRepository:

    @staticmethod
    def add(candidate: Candidate):
        db.session.add(candidate)

    @staticmethod
    def get(candidate_id: str):
        return Candidate.query.get(candidate_id)

    @staticmethod
    def get_by_email(email: str):
        return Candidate.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def get_all():
        return Candidate.query.all()

    @staticmethod
    def delete(candidate: Candidate):
        db.session.delete(candidate)