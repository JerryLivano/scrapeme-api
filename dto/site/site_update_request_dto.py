class SiteUpdateRequestDto:
    def __init__(self, guid: str, categories_guid: list[str], site_name: str, site_url: str, url_pattern: list[dict],
                 data_url_pattern: list[dict] | None = None, space_rule: str | None = None):
        self.guid = guid
        self.categories_guid = categories_guid
        self.site_name = site_name
        self.site_url = site_url
        self.space_rule = space_rule
        self.url_pattern = url_pattern
        self.data_url_pattern = data_url_pattern
