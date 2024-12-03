class TemplateRequestDto:
    def __init__(self, container: str | None, container_tag: str, site_guid: str, tag_data: list[dict], is_class: bool | None,
                 is_id: bool | None):
        self.site_guid = site_guid
        self.container = container
        self.container_tag = container_tag
        self.is_class = is_class
        self.is_id = is_id
        self.tag_data = tag_data
