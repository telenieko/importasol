class ImportaSOLError(Exception):
    pass


class ValidationError(ImportaSOLError):
    pass


class ProgrammingError(ImportaSOLError):
    pass
