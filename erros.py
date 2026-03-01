class HttpError(Exception):

    def __init__(self, code: int, message: str | dict | list):
        self.code = code
        self.message = message
