from database.db import db

from datetime import datetime
import uuid


class Interview(db.Model):

    __tablename__ = "interviews"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    candidate_id = db.Column(
        db.String(36),
        db.ForeignKey("candidates.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="In Progress"
    )

    started_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ended_at = db.Column(
        db.DateTime,
        nullable=True
    )

    current_question_number = db.Column(
        db.Integer,
        default=1
    )

    total_questions = db.Column(
        db.Integer,
        default=10
    )

    current_question = db.Column(
        db.Text,
        nullable=True
    )

    # ----------------------------
    # Relationships
    # ----------------------------

    candidate = db.relationship(
        "Candidate",
        back_populates="interviews"
    )

    questions = db.relationship(
        "InterviewQuestion",
        back_populates="interview",
        cascade="all, delete-orphan",
        lazy=True
    )

    report = db.relationship(
        "InterviewReport",
        back_populates="interview",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return f"<Interview {self.id}>"