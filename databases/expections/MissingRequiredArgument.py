class MissingRequiredArgrument(Exception):
    def __init__(self):
        self.message = "Expected a missing argrument"
        super().__init__(self.message)