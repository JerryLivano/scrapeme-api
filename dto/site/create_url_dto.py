class CreateUrlDto:
    def __init__(self, site_url: str, space_rule: str, url_pattern: list[dict]):
        self.site_url = site_url
        self.space_rule = space_rule
        self.url_pattern = url_pattern