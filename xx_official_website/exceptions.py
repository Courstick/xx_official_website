# -*- coding:utf-8 -*-

class BusinessException(Exception):
    code = 5000
    message = "System Error"

    def __init__(self, code=None, message=None, error_data=None):
        self.code = code or self.code
        self.message = message or self.message
        self.error_data = error_data


def raise_business_error_if(condition, code=None, message=None, error_data=None):
    """ 检查条件, 如果不为真, 则抛出BusinessException
    Args:
        condition:
        code:
        message:
        error_data:
    Returns:
    """
    if condition:
        raise BusinessException(code, message, error_data)
