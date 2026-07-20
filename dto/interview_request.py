"""
dto/interview_request.py

Contains the data required to start a new interview.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class InterviewRequest:
    """
    DTO used to initialize a new interview.
    """

    full_name: str
    email: str
    target_role: str
    experience: str
    interview_type: str
    difficulty: str

    total_questions: int = 10