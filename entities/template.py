class Template:
    def __init__(self, guid: str, container: str | None, container_tag: str, is_class: bool, is_id: bool,
                 site_guid: str, tag_data: list[dict]):
        self.guid = guid
        self.container = container
        self.container_tag = container_tag
        self.is_class = is_class
        self.is_id = is_id
        self.site_guid = site_guid
        self.tag_data = tag_data

    def to_dict(self):
        return {
            'guid': self.guid,
            'container': self.container,
            'container_tag': self.container_tag,
            'is_class': self.is_class,
            'is_id': self.is_id,
            'site_guid': self.site_guid,
            'tag_data': self.tag_data
        }
