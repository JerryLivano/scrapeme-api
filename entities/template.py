class Template:
    def __init__(self, guid: str, site_guid: str, tag_data: list[dict]):
        self.guid = guid
        self.site_guid = site_guid
        self.tag_data = tag_data

    def to_dict(self):
        return {
            'guid': self.guid,
            'site_guid': self.site_guid,
            'tag_data': self.tag_data
        }