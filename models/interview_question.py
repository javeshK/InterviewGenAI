from datetime import datetime
import uuid

from database.db import db


class InterviewQuestion(db.Model):
    """
    Represents a single question-answer pair in an interview.

    One Interview consists of multiple InterviewQuestions.
    Each record stores:
        - AI generated question
        - Candidate's answer
        - Ideal answer
        - AI evaluation
        - Scores
    """

    __tablename__ = "interview_questions"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    interview_id = db.Column(
        db.String(36),
        db.ForeignKey("interviews.id"),
        nullable=False
    )

    question_number = db.Column(
        db.Integer,
        nullable=False
    )

    # -----------------------------
    # Interview Content
    # -----------------------------

    question = db.Column(
        db.Text,
        nullable=False
    )

    candidate_answer = db.Column(
        db.Text,
        nullable=True
    )

    ideal_answer = db.Column(
        db.Text,
        nullable=True
    )

    feedback = db.Column(
        db.Text,
        nullable=True
    )

    # -----------------------------
    # AI Evaluation Scores
    # -----------------------------

    technical_score = db.Column(
        db.Float,
        default=0.0
    )

    communication_score = db.Column(
        db.Float,
        default=0.0
    )

    confidence_score = db.Column(
        db.Float,
        default=0.0
    )

    overall_score = db.Column(
        db.Float,
        default=0.0
    )

    # -----------------------------
    # Metadata
    # -----------------------------

    answered_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -----------------------------
    # Relationships
    # -----------------------------

    interview = db.relationship(
        "Interview",
        back_populates="questions"
    )

    # -----------------------------
    # Utility Methods
    # -----------------------------

    @property
    def is_answered(self):
        """
        Returns True if the candidate has answered this question.
        """
        return bool(self.candidate_answer)

    def __repr__(self):
        return (
            f"<InterviewQuestion("
            f"{self.question_number}, "
            f"Interview={self.interview_id})>"
        )