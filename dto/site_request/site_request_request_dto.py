class SiteRequestRequestDto:
    def __init__(self, account_guid: str, subject: str, site_url: str, description: str):
        self.account_guid = account_guid
        self.subject = subject
        self.site_url = site_url
        self.description = description