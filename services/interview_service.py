from database.db import db

from models.interview_session import InterviewSession
from models.conversation_message import ConversationMessage

from repositories.candidate_repository import CandidateRepository
from repositories.interview_repository import InterviewRepository
from repositories.interview_question_repository import (
    InterviewQuestionRepository
)

from services.llm_service import LLMService
from services.session_manager import SessionManager


class InterviewService:

    def __init__(self):
        self.llm = LLMService()

    def start_interview(
        self,
        name,
        email,
        role,
        experience,
        interview_type,
        difficulty
    ):

        try:

            candidate = CandidateRepository.create(
                name,
                email
            )

            interview = InterviewRepository.create(

                candidate.id,

                role,

                experience,

                interview_type,

                difficulty
            )

            session = InterviewSession(

                interview_id=interview.id,

                candidate_name=name,

                role=role,

                experience=experience,

                interview_type=interview_type,

                difficulty=difficulty
            )

            SessionManager.add_session(session)

            question = self.llm.generate_first_question(
                session
            )

            InterviewQuestionRepository.create(

                interview.id,

                1,

                question
            )

            session.current_question = question

            session.question_number = 1

            session.history.append(

                ConversationMessage(

                    role="assistant",

                    content=question
                )
            )

            db.session.commit()

            return session

        except Exception:

            db.session.rollback()

            raise