from database.db import db
from models.interview_report import InterviewReport


class ReportRepository:

    @staticmethod
    def create(interview_id):

        report = InterviewReport(

            interview_id=interview_id
        )

        db.session.add(report)

        return report

    @staticmethod
    def save():

        db.session.commit()