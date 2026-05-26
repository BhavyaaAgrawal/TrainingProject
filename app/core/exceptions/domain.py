class AppError(Exception):
    def __init__(self, code:str, message:str, *, details:dict | None = None):
        # passing message to base class inherited here ie Exception
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

class NotFoundError(AppError):
    pass

class ConflictError(AppError):
    pass

class AuthError(AppError):
    pass

class IncorrectPasswordError(AppError):
    pass