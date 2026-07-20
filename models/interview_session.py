"""
interview_session.py

Runtime interview session object.

This class is NOT stored in the database.

Purpose
-------
Acts as the working memory for InterviewService during an interview.

Contains:
- Candidate
- Interview
- Current Question
- Question History

The database remains the source of truth, while this object
makes business logic much cleaner.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from models.candidate import Candidate
from models.interview import Interview
from models.interview_question import InterviewQuestion


@dataclass
class InterviewSession:
    """
    Runtime interview session.

    This object exists only while InterviewService is executing.
    """

    candidate: Candidate

    interview: Interview

    current_question: Optional[InterviewQuestion] = None

    history: List[InterviewQuestion] = field(default_factory=list)

    # -----------------------------
    # Helper Methods
    # -----------------------------

    def add_question(
        self,
        question: InterviewQuestion
    ) -> None:
        """
        Add a newly generated question to history.
        """

        self.history.append(question)
        self.current_question = question

    def get_question_count(self) -> int:
        """
        Returns number of generated questions.
        """

        return len(self.history)

    def has_questions(self) -> bool:
        """
        Returns True if at least one question exists.
        """

        return len(self.history) > 0

    def is_finished(self) -> bool:
        """
        Check whether interview has reached its limit.
        """

        return (
            self.interview.current_question_number
            >=
            self.interview.total_questions
        )

    def current_question_number(self) -> int:
        """
        Returns current interview question number.
        """

        return self.interview.current_question_number

    def next_question_number(self) -> int:
        """
        Returns the next question number.
        """

        return self.interview.current_question_number + 1

    def increment_question(self) -> None:
        """
        Move interview to the next question.
        """

        self.interview.current_question_number += 1
        self.interview.completed_questions += 1

    def get_latest_question(self) -> Optional[InterviewQuestion]:
        """
        Returns the most recently asked question.
        """

        return self.current_question

    def set_current_question(
        self,
        question: InterviewQuestion
    ) -> None:
        """
        Set current active question.
        """

        self.current_question = question

    def complete(self) -> None:
        """
        Mark interview as completed.
        """

        self.interview.status = "Completed"

    def cancel(self) -> None:
        """
        Cancel interview.
        """

        self.interview.status = "Cancelled"

    def reset(self) -> None:
        """
        Clears runtime state.
        """

        self.current_question = None
        self.history.clear()

    def __repr__(self) -> str:

        return (
            f"<InterviewSession("
            f"candidate='{self.candidate.full_name}', "
            f"role='{self.candidate.target_role}', "
            f"question={self.interview.current_question_number}, "
            f"status='{self.interview.status}')>"
        )