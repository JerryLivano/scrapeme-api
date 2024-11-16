class SiteUpdateActiveDto:
    def __init__(self, guid: str, is_active: bool):
        self.guid = guid
        self.is_active = is_active