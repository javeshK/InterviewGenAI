from dataclasses import dataclass, field

from models.conversation_message import ConversationMessage


@dataclass
class InterviewSession:

    interview_id: int

    candidate_name: str

    role: str

    experience: str

    interview_type: str

    difficulty: str

    question_number: int = 0

    current_question: str = ""

    history: list[ConversationMessage] = field(default_factory=list)

    technical_scores: list[float] = field(default_factory=list)

    communication_scores: list[float] = field(default_factory=list)

    confidence_scores: list[float] = field(default_factory=list)