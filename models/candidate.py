from database.db import db

from datetime import datetime
import uuid


class Candidate(db.Model):

    __tablename__ = "candidates"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=True
    )

    target_role = db.Column(
        db.String(120),
        nullable=False
    )

    experience = db.Column(
        db.String(50),
        nullable=False
    )

    interview_type = db.Column(
        db.String(50),
        nullable=False
    )

    difficulty = db.Column(
        db.String(30),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    interviews = db.relationship(
        "Interview",
        back_populates="candidate",
        lazy=True
    )

    def __repr__(self):
        return f"<Candidate {self.full_name}>"