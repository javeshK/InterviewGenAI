from models.interview_report import InterviewReport


class InterviewReportRepository:

    @staticmethod
    def create(report):

        return report

    @staticmethod
    def get(report_id):

        return InterviewReport.query.get(report_id)

    @staticmethod
    def get_by_interview(interview_id):

        return InterviewReport.query.filter_by(
            interview_id=interview_id
        ).first()