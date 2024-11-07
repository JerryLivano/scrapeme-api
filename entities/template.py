class Template:
    def __init__(self, guid: str, container: str | None, is_class: bool, is_id: bool, is_tag: bool,
                 site_guid: str, tag_data: list[dict]):
        self.guid = guid
        self.container = container
        self.is_class = is_class
        self.is_id = is_id
        self.is_tag = is_tag
        self.site_guid = site_guid
        self.tag_data = tag_data

    def to_dict(self):
        return {
            'guid': self.guid,
            'container': self.container,
            'is_class': self.is_class,
            'is_id': self.is_id,
            'is_tag': self.is_tag,
            'site_guid': self.site_guid,
            'tag_data': self.tag_data
        }
