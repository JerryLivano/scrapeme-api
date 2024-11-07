class SiteRequestDto:
    def __init__(self, admin_guid: str, site_name: str, site_url: str,
                 url_pattern: list[dict], data_url_pattern: list[dict] | None = None, space_rule: str | None = None):
        self.admin_guid = admin_guid
        self.site_name = site_name
        self.site_url = site_url
        self.space_rule = space_rule
        self.url_pattern = url_pattern
        self.data_url_pattern = data_url_pattern
