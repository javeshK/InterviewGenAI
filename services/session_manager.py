from models.interview_session import InterviewSession


class SessionManager:

    _sessions = {}

    @classmethod
    def add_session(cls, session: InterviewSession):

        cls._sessions[session.interview_id] = session

    @classmethod
    def get_session(cls, interview_id):

        return cls._sessions.get(interview_id)

    @classmethod
    def update_session(cls, session: InterviewSession):

        cls._sessions[session.interview_id] = session

    @classmethod
    def remove_session(cls, interview_id):

        cls._sessions.pop(interview_id, None)

    @classmethod
    def active_sessions(cls):

        return len(cls._sessions)