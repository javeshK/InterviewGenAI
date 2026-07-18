from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConversationMessage:

    role: str

    content: str

    timestamp: datetime = datetime.now()    