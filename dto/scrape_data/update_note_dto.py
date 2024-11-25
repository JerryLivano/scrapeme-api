class UpdateNoteDto:
    def __init__(self, guid: str, index: int, note: str):
        self.guid = guid
        self.index = index
        self.note = note