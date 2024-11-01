class SiteRequestUpdateRequestDto:
    def __init__(self, guid: str, subject: str, site_url: str, description: str):
        self.guid = guid
        self.subject = subject
        self.site_url = site_url
        self.description = description