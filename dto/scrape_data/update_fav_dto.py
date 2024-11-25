class UpdateFavDto:
    def __init__(self, guid: str, index: int, is_favourite: bool):
        self.guid = guid
        self.index = index
        self.is_favourite = is_favourite