from database.db import db

from datetime import datetime
import uuid


class InterviewReport(db.Model):

    __tablename__ = "interview_reports"

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

    overall_score = db.Column(
        db.Float,
        default=0
    )

    technical_score = db.Column(
        db.Float,
        default=0
    )

    communication_score = db.Column(
        db.Float,
        default=0
    )

    confidence_score = db.Column(
        db.Float,
        default=0
    )

    strengths = db.Column(
        db.Text
    )

    weaknesses = db.Column(
        db.Text
    )

    recommendations = db.Column(
        db.Text
    )

    final_summary = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    interview = db.relationship(
        "Interview",
        back_populates="report"
    )