from .companies_datastore import CompaniesDatastore
from .notification import Notification


class NotificationsDatastore(CompaniesDatastore):
    def __init__(self):
        super(NotificationsDatastore, self).__init__()

    def get_company_notifications(self, company_id: str, user_language: str) -> list[Notification]:
        company_document_reference = self.db.collection('companies').document(company_id)
        company_snapshot = company_document_reference.get(('content_languages_iso',))
        company_languages = company_snapshot.to_dict().get('content_languages_iso')
        notifications = company_document_reference.collection('notifications').get()
        for notification in notifications:
            yield Notification(notification.id, notification.to_dict(), user_language, company_languages)
