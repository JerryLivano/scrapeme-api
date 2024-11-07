class TemplateUpdateRequestDto:
    def __init__(self, guid: str, container: str | None, is_class: bool, is_id: bool, is_tag: bool,
                 tag_data: list[dict]):
        self.guid = guid
        self.container = container
        self.is_class = is_class
        self.is_id = is_id
        self.is_tag = is_tag
        self.tag_data = tag_data
