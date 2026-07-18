from app import app

from repositories.candidate_repository import CandidateRepository

with app.app_context():

    candidate = CandidateRepository.create(

        name="Javesh Khosla",

        email="newnew@test.com"
    )

    print(candidate.id)

    print(candidate.name)