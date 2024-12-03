class CreateSiteUrlDto:
    def __init__(self, site_url: str, url_pattern: list[dict], space_rule: str):
        self.site_url = site_url
        self.url_pattern = url_pattern
        self.space_rule = space_rule
