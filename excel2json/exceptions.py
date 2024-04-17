

class MissingRequiredFieldError(Exception):
    def __init__(self, field_names):
        self.field_names = field_names
        super().__init__(f"Required field '{','.join(field_names)}' is missing.")