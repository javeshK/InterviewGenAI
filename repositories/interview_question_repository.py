from database.db import db
from models.interview_question import InterviewQuestion


class InterviewQuestionRepository:
    """
    Repository responsible for InterviewQuestion database operations.

    NOTE:
    This repository NEVER commits transactions.
    Transaction management is handled by InterviewService.
    """

    @staticmethod
    def create(
        interview_id: str,
        question_number: int,
        question: str
    ) -> InterviewQuestion:
        """
        Create a new interview question object.

        Returns the object without committing.
        """

        interview_question = InterviewQuestion(
            interview_id=interview_id,
            question_number=question_number,
            question=question
        )

        return interview_question

    @staticmethod
    def get(question_id: str) -> InterviewQuestion | None:
        """
        Get a question by its ID.
        """

        return InterviewQuestion.query.get(question_id)

    @staticmethod
    def get_by_interview(interview_id: str) -> list[InterviewQuestion]:
        """
        Return all questions belonging to an interview.
        """

        return (
            InterviewQuestion.query
            .filter_by(interview_id=interview_id)
            .order_by(InterviewQuestion.question_number.asc())
            .all()
        )

    @staticmethod
    def get_by_number(
        interview_id: str,
        question_number: int
    ) -> InterviewQuestion | None:
        """
        Get a specific question number for an interview.
        """

        return (
            InterviewQuestion.query
            .filter_by(
                interview_id=interview_id,
                question_number=question_number
            )
            .first()
        )

    @staticmethod
    def get_latest(interview_id: str) -> InterviewQuestion | None:
        """
        Return the most recently asked question.
        """

        return (
            InterviewQuestion.query
            .filter_by(interview_id=interview_id)
            .order_by(
                InterviewQuestion.question_number.desc()
            )
            .first()
        )

    @staticmethod
    def get_all() -> list[InterviewQuestion]:
        """
        Return every interview question.
        """

        return InterviewQuestion.query.all()

    @staticmethod
    def delete(question: InterviewQuestion) -> None:
        """
        Delete a question object.
        """

        db.session.delete(question)