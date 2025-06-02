class BusinessException(Exception):
    def __init__(self, code: int = 1000, msg: str = "business exception"):
        self.code = code
        self.msg = msg
        super().__init__(msg)


class UserExistException(BusinessException):
    def __init__(self, code: int = 2001, msg: str = "user already exist"):
        super().__init__(code, msg)


class UserNotExistException(BusinessException):
    def __init__(self, code: int = 2002, msg: str = "user not exist"):
        super().__init__(code, msg)


class UserPasswordInvalidException(BusinessException):
    def __init__(self, code: int = 2003, msg: str = "user password invalid"):
        super().__init__(code, msg)


class ChatExistException(BusinessException):
    def __init__(self, code: int = 3001, msg: str = "chat already exist"):
        super().__init__(code, msg)

class ChatDeletedException(BusinessException):
    def __init__(self, code: int = 3002, msg: str = "chat already deleted"):
        super().__init__(code, msg)
