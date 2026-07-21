"""
services/interview_service.py

Application Service responsible for the complete interview workflow.

Responsibilities
----------------
• Validate incoming interview requests
• Create Candidate
• Create Interview
• Generate AI questions
• Persist interview data
• Manage transactions
• Coordinate repositories and AI services

Version 1
----------
✓ Start Interview
✓ Create Candidate
✓ Create Interview
✓ Generate First Question
✓ Save First Question

Version 2
----------
- Submit Answer
- Evaluate Answer
- Generate Next Question
- Finish Interview
"""

from __future__ import annotations

import logging
from datetime import datetime

from database.db import db

from dto.interview_request import InterviewRequest

from enums.interview_status import InterviewStatus
from enums.question_type import QuestionType

from models.candidate import Candidate
from models.interview import Interview
from models.interview_question import InterviewQuestion

from repositories.candidate_repository import CandidateRepository
from repositories.interview_repository import InterviewRepository
from repositories.interview_question_repository import (
    InterviewQuestionRepository,
)
from repositories.interview_report_repository import (
    InterviewReportRepository,
)

from services.llm_service import LLMService
from services.evaluation_service import EvaluationService


logger = logging.getLogger(__name__)


class InterviewService:
    """
    Coordinates the interview workflow.

    Routes
        ↓

    InterviewService
        ↓

    Repositories
        ↓

    SQLite

        +

    Gemini AI
    """

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(
        self,
        candidate_repository: CandidateRepository | None = None,
        interview_repository: InterviewRepository | None = None,
        question_repository: InterviewQuestionRepository | None = None,
        report_repository: InterviewReportRepository | None = None,
        llm_service: LLMService | None = None,
        evaluation_service: EvaluationService | None = None,
    ):

        self.candidate_repository = (
            candidate_repository or CandidateRepository()
        )

        self.interview_repository = (
            interview_repository or InterviewRepository()
        )

        self.question_repository = (
            question_repository or InterviewQuestionRepository()
        )

        self.report_repository = (
            report_repository or InterviewReportRepository()
        )

        self.llm = llm_service or LLMService()

        self.evaluation_service = (
            evaluation_service or EvaluationService()
        )

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate_request(
        self,
        request: InterviewRequest,
    ) -> None:
        """
        Validate interview request before creating entities.
        """

        if not request.full_name.strip():
            raise ValueError("Candidate name is required.")

        if not request.target_role.strip():
            raise ValueError("Target role is required.")

        if request.total_questions <= 0:
            raise ValueError(
                "Total questions must be greater than zero."
            )

    # ==========================================================
    # Transaction Helpers
    # ==========================================================

    def _commit(self) -> None:

        try:

            db.session.commit()

            logger.info("Transaction committed successfully.")

        except Exception:

            logger.exception("Database commit failed.")

            db.session.rollback()

            raise

    def _rollback(self) -> None:

        logger.warning("Transaction rolled back.")

        db.session.rollback()

    # ==========================================================
    # Candidate Helpers
    # ==========================================================

    def _create_candidate(
        self,
        request: InterviewRequest,
    ) -> Candidate:
        """
        Creates and persists a Candidate.
        """

        logger.info(
            "Creating candidate '%s'",
            request.full_name,
        )

        candidate = Candidate(

            full_name=request.full_name,

            email=request.email,

            target_role=request.target_role,

            experience=request.experience,

            interview_type=request.interview_type,

            difficulty=request.difficulty,

        )

        self.candidate_repository.add(candidate)

        return candidate

    # ==========================================================
    # Interview Helpers
    # ==========================================================

    def _create_interview(
        self,
        candidate: Candidate,
        request: InterviewRequest,
    ) -> Interview:
        """
        Creates Interview entity.
        """

        logger.info(
            "Creating interview for %s",
            candidate.full_name,
        )

        interview = Interview(

            candidate=candidate,

            status=InterviewStatus.IN_PROGRESS.value,

            started_at=datetime.utcnow(),

            current_question_number=1,

            completed_questions=0,

            total_questions=request.total_questions,

        )

        self.interview_repository.add(interview)

        return interview

    # ==========================================================
    # AI Helpers
    # ==========================================================

    def _generate_first_question(
        self,
        candidate: Candidate,
    ) -> str:
        """
        Generate first interview question using Gemini.
        """

        logger.info("Generating first AI question...")

        question = self.llm.generate_first_question(
            candidate
        )

        logger.info("First question generated successfully.")

        return question

    # ==========================================================
    # Question Helpers
    # ==========================================================

    def _create_first_question(
        self,
        interview: Interview,
        question_text: str,
    ) -> InterviewQuestion:
        """
        Creates the first InterviewQuestion.
        """

        logger.info("Creating first interview question.")

        question = InterviewQuestion(

            interview=interview,

            question_number=1,

            question_type=QuestionType.TECHNICAL.value,

            question=question_text,

            candidate_answer=None,

            ideal_answer=None,

            feedback=None,

            technical_score=0,

            communication_score=0,

            confidence_score=0,

            overall_score=0,

        )

        self.question_repository.add(question)

        interview.current_question = question_text

        return question

    # ==========================================================
    # Public API
    # ==========================================================

    def start_interview(
        self,
        request: InterviewRequest,
    ) -> Interview:
        """
        Starts a new interview.

        Workflow

        Validate Request
                ↓

        Create Candidate
                ↓

        Create Interview
                ↓

        Generate First Question
                ↓

        Save Question
                ↓

        Commit
                ↓

        Return Interview
        """

        logger.info(
            "Starting interview for '%s'",
            request.full_name,
        )

        try:

            self._validate_request(request)

            candidate = self._create_candidate(
                request
            )

            interview = self._create_interview(
                candidate,
                request,
            )

            first_question = (
                self._generate_first_question(
                    candidate
                )
            )

            self._create_first_question(
                interview,
                first_question,
            )

            self._commit()
            logger.info(
                "Interview successfully created for '%s'",
                request.full_name,
            )

            return interview

        except Exception as exc:

            logger.exception(
                "Failed to start interview."
            )

            self._rollback()

            raise RuntimeError(
                "Unable to start interview."
            ) from exc

    # ==========================================================
    # Retrieval Methods
    # ==========================================================

    def get_interview(
        self,
        interview_id: int,
    ) -> Interview | None:
        """
        Retrieve an interview by its ID.
        """

        logger.info(
            "Fetching interview (ID=%s)",
            interview_id,
        )

        return self.interview_repository.get(
            interview_id
        )

    def get_current_question(
        self,
        interview_id: int,
    ) -> InterviewQuestion | None:
        """
        Returns the current active interview question.
        """

        logger.info(
            "Fetching current question for interview %s",
            interview_id,
        )

        interview = self.get_interview(
            interview_id
        )

        if interview is None:

            logger.warning(
                "Interview %s does not exist.",
                interview_id,
            )

            return None

        return self.question_repository.get_latest(
            interview_id
        )

    def get_question_history(
        self,
        interview_id: int,
    ) -> list[InterviewQuestion]:
        """
        Returns every question belonging
        to an interview.
        """

        logger.info(
            "Loading interview history (%s)",
            interview_id,
        )

        return self.question_repository.get_by_interview(
            interview_id
        )

    # ==========================================================
    # Status Helpers
    # ==========================================================

    def interview_exists(
        self,
        interview_id: int,
    ) -> bool:
        """
        Returns True if the interview exists.
        """

        return (
            self.get_interview(interview_id)
            is not None
        )

    def is_interview_completed(
        self,
        interview: Interview,
    ) -> bool:
        """
        Check if all interview questions
        have been completed.
        """

        return (
            interview.completed_questions
            >= interview.total_questions
        )

    def remaining_questions(
        self,
        interview: Interview,
    ) -> int:
        """
        Returns the number of remaining questions.
        """

        remaining = (
            interview.total_questions
            - interview.completed_questions
        )

        return max(remaining, 0)

    # ==========================================================
    # Internal Helpers
    # ==========================================================

    def _update_current_question(
        self,
        interview: Interview,
        question_text: str,
    ) -> None:
        """
        Update the interview's current question.
        """

        interview.current_question = question_text

    def _increment_question_counter(
        self,
        interview: Interview,
    ) -> None:
        """
        Move the interview forward by one question.
        """

        interview.current_question_number += 1
        interview.completed_questions += 1

    def _mark_completed(
        self,
        interview: Interview,
    ) -> None:
        """
        Mark an interview as completed.
        """

        interview.status = (
            InterviewStatus.COMPLETED.value
        )

        interview.ended_at = datetime.utcnow()

    def _mark_cancelled(
        self,
        interview: Interview,
    ) -> None:
        """
        Mark an interview as cancelled.
        """

        interview.status = (
            InterviewStatus.CANCELLED.value
        )

        interview.ended_at = datetime.utcnow()

    # ==========================================================
    # Future Version Placeholders
    # ==========================================================

    def submit_answer(self, *args, **kwargs):
        """
        Version 2

        Evaluate candidate answer,
        generate the next question,
        and update interview progress.
        """

        raise NotImplementedError(
            "submit_answer() will be implemented in Version 2."
        )

    def finish_interview(self, *args, **kwargs):
        """
        Version 3

        Generate report,
        calculate final scores,
        and persist InterviewReport.
        """

        raise NotImplementedError(
            "finish_interview() will be implemented in Version 3."
        )
        # ==========================================================
    # Interview Loop
    # ==========================================================

    def submit_answer(
        self,
        interview_id: int,
        answer: str,
    ):
        """
        Submit the candidate's answer.

        Workflow

        Load Interview
                ↓
        Load Current Question
                ↓
        Save Candidate Answer
                ↓
        Gemini Evaluation
                ↓
        Validate Scores
                ↓
        Save Evaluation
                ↓
        Finished?

          Yes          No

        Report     Next Question
        """

        logger.info(
            "Submitting answer for interview %s",
            interview_id,
        )

        try:

            # -----------------------------------
            # Load Interview
            # -----------------------------------

            interview = self.get_interview(
                interview_id
            )

            if interview is None:

                raise ValueError(
                    "Interview not found."
                )

            # -----------------------------------
            # Load Current Question
            # -----------------------------------

            current_question = (
                self.question_repository.get_latest(
                    interview_id
                )
            )

            if current_question is None:

                raise ValueError(
                    "No active question found."
                )

            # -----------------------------------
            # Save Candidate Answer
            # -----------------------------------

            current_question.candidate_answer = answer
            current_question.answered_at = datetime.utcnow()

            # -----------------------------------
            # AI Evaluation
            # -----------------------------------

            logger.info(
                "Evaluating answer using Gemini."
            )

            evaluation = self.llm.evaluate_answer(

                question=current_question.question,

                answer=answer,

                candidate=interview.candidate,

            )

            # -----------------------------------
            # Validate AI Output
            # -----------------------------------

            self.evaluation_service.validate_evaluation(
                    evaluation)

            # -----------------------------------
            # Save Scores
            # -----------------------------------

            current_question.technical_score = (
                evaluation["technical_score"]
            )

            current_question.communication_score = (
                evaluation["communication_score"]
            )

            current_question.confidence_score = (
                evaluation["confidence_score"]
            )

            current_question.overall_score = (
                evaluation["overall_score"]
            )

            current_question.feedback = (
                evaluation["feedback"]
            )

            current_question.ideal_answer = (
                evaluation["ideal_answer"]
            )

            interview.completed_questions += 1

            # -----------------------------------
            # Finished?
            # -----------------------------------

            if (
                interview.completed_questions
                >= interview.total_questions
            ):

                logger.info(
                    "Interview completed."
                )

                self._mark_completed(
                    interview
                )

                self._commit()

                return {

    "completed": True,

    "interview": interview,

    "feedback": current_question.feedback,

    "technical_score": current_question.technical_score,

    "communication_score": current_question.communication_score,

    "confidence_score": current_question.confidence_score,

    "overall_score": current_question.overall_score,

}
            # -----------------------------------
            # Generate Next Question
            # -----------------------------------

            logger.info(
                "Generating next interview question."
            )

            history = (
                self.question_repository.get_by_interview(
                    interview_id
                )
            )

            next_question_text = (
                self.llm.generate_followup_question(

                candidate=interview.candidate,

                history=history,

                )
            )

            next_question = InterviewQuestion(

                interview=interview,

                question_number=(
                    interview.completed_questions + 1
                ),

                question_type=QuestionType.TECHNICAL.value,

                question=next_question_text,

            )

            self.question_repository.add(
                next_question
            )

            interview.current_question_number += 1
            interview.current_question = next_question_text

            self._commit()

            logger.info(
                "Next question generated successfully."
            )

            return {

    "completed": False,

    "question": next_question,

    "interview": interview,

    "feedback": evaluation["feedback"],

    "technical_score": evaluation["technical_score"],

    "communication_score": evaluation["communication_score"],

    "confidence_score": evaluation["confidence_score"],

    "overall_score": evaluation["overall_score"],

}

        except Exception as exc:

            logger.exception(
                "Error while submitting answer."
            )

            self._rollback()

            raise RuntimeError(
                "Unable to process interview answer."
            ) from exc                  