class WebDataAnalysisDto:
    def __init__(self, sort_bedroom: list[dict], sort_bathroom: list[dict], sort_surface: list[dict],
                 sort_building: list[dict]):
        self.sort_bedroom = sort_bedroom
        self.sort_bathroom = sort_bathroom
        self.sort_surface = sort_surface
        self.sort_building = sort_building
