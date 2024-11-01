class SiteRequestDeclineDto:
    def __init__(self, guid: str, decline_reason: str):
        self.guid = guid
        self.decline_reason = decline_reason