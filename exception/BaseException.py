class BaseException:
    def __init__(self, errorcode, message):
        self.errorcode = errorcode
        self.message = message