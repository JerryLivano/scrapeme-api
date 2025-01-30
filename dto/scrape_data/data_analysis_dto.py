class DataAnalysisDto:
    def __init__(self, avg_bedroom: int, avg_bathroom: int, avg_building: int, avg_surface: int, data_count: int):
        self.avg_bedroom = avg_bedroom
        self.avg_bathroom = avg_bathroom
        self.avg_building = avg_building
        self.avg_surface = avg_surface
        self.data_count = data_count