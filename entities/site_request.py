from datetime import datetime

class SiteRequest:
    def __init__(self, guid: str, account_guid: str, subject: str, site_url: str, description: str,
                 status: int, decline_reason: str | None, created_date: datetime, updated_date: datetime | None):
        self.guid = guid
        self.account_guid = account_guid
        self.subject = subject
        self.site_url = site_url
        self.description = description
        self.status = status
        self.decline_reason = decline_reason
        self.created_date = created_date
        self.updated_date = updated_date

    def to_dict(self):
        return {
            'guid': self.guid,
            'account_guid': self.account_guid,
            'subject': self.subject,
            'site_url': self.site_url,
            'description': self.description,
            'status': self.status,
            'decline_reason': self.decline_reason,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }
