

class MissingRequiredFieldError(Exception):
    def __init__(self, field_names):
        self.field_names = field_names
        super().__init__(f"Required field '{','.join(field_names)}' is missing.")

class MissingRequiredCellError(Exception):
    def __init__(self, cell_name):
        self.cell_name = cell_name
        super().__init__(f"Required cell {cell_name} is missing.")