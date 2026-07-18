from models.candidate import Candidate


class CandidateRepository:

    @staticmethod
    def create(candidate):

        return candidate

    @staticmethod
    def get(candidate_id):

        return Candidate.query.get(candidate_id)

    @staticmethod
    def get_by_email(email):

        return Candidate.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def get_all():

        return Candidate.query.all()