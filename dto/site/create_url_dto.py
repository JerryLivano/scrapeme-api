class CreateUrlDto:
    def __init__(self, url: str | None, data_url: str | None):
        self.url = url
        self.data_url = data_url