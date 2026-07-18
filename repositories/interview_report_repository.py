from database.db import db
from models.interview_report import InterviewReport


class InterviewReportRepository:

    @staticmethod
    def add(report: InterviewReport):
        db.session.add(report)

    @staticmethod
    def get(report_id: str):
        return InterviewReport.query.get(report_id)

    @staticmethod
    def get_by_interview(interview_id: str):

        return (
            InterviewReport.query
            .filter_by(interview_id=interview_id)
            .first()
        )

    @staticmethod
    def delete(report: InterviewReport):
        db.session.delete(report)