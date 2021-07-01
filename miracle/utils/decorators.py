"""
This module defines helper decorators
"""


def middleware(fn):
    """This decorator is used for implement any action
    before processing the API"""
    def inner(*args, **kwargs):
        print('before execution')
        response = fn(*args, **kwargs)
        print(response.get('status_code'))
        print('after execution')
        return response
    return inner
