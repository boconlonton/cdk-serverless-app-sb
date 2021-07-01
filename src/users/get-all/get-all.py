"""
This is the handler for user/get
"""
from miracle.utils.decorators import middleware


@middleware(loggig=False)
def handler(event, context):
    pass


print(handler({}, {}))
