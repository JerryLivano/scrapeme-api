class TemplateRequestDto:
    def __init__(self, container: str | None, site_guid: str, tag_data: list[dict], is_class: bool | None,
                 is_id: bool | None, is_tag: bool | None):
        self.site_guid = site_guid
        self.container = container
        self.is_class = is_class
        self.is_id = is_id
        self.is_tag = is_tag
        self.tag_data = tag_data
