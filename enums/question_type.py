"""
enums/question_type.py

Question category definitions.
"""

from enum import Enum


class QuestionType(str, Enum):
    """
    Supported interview question types.
    """

    TECHNICAL = "Technical"

    HR = "HR"

    BEHAVIOURAL = "Behavioural"

    CODING = "Coding"

    SYSTEM_DESIGN = "System Design"

    RESUME = "Resume"

    GENERAL = "General"

    FOLLOW_UP = "Follow-up"

    @classmethod
    def values(cls):
        """
        Returns all enum values.
        """

        return [question.value for question in cls]