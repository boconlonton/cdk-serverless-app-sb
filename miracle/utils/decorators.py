"""
This module defines helper decorators
"""


def middleware(*args, **kwargs):
    def inner(fn):
        """This decorator is used for implement any action
        before processing the API"""
        def wrapper(*args, **kwargs):
            print('before execution')
            print(args)
            print(kwargs)
            response = fn(*args, **kwargs)
            print('after execution')
            return response
        return wrapper
    return inner
