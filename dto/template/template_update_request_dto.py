class TemplateUpdateRequestDto:
    def __init__(self, guid: str, container: str | None, container_tag: str, is_class: bool, is_id: bool,
                 tag_data: list[dict]):
        self.guid = guid
        self.container = container
        self.container_tag = container_tag
        self.is_class = is_class
        self.is_id = is_id
        self.tag_data = tag_data
