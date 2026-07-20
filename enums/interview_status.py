"""
enums/interview_status.py

Interview status values.
"""

from enum import Enum


class InterviewStatus(str, Enum):
    """
    Possible interview states.
    """

    PENDING = "Pending"

    IN_PROGRESS = "In Progress"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"

    FAILED = "Failed"

    PAUSED = "Paused"

    @classmethod
    def values(cls):
        """
        Returns all enum values.
        """

        return [status.value for status in cls]