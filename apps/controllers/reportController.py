from apps.db.repositories.ReportRepository import reportRepository

class reportController:
    @classmethod
    def get_product_bills(cls, connection):
        return reportRepository.get_product_bills(connection)

    @classmethod
    def get_general_reports(cls, connection, group_by):
        return reportRepository.get_general_reports(connection, group_by)
