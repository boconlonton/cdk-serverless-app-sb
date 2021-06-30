"""
This module defines the default template for API Gateway respons
"""

# DEFAULT API GATEWAY RESPONSE HEADER
HEADER = {
    'Access-Control-Allow-Headers': "'*'",
    'Access-Control-Allow-Methods': "'*'",
    'Access-Control-Allow-Origin': "'*'",
}

# DEFAULT API GATEWAY RESPONSE BODY FOR 4XX STATUS CODE
RESPONSE_4XX = '''{
    "message": "$context.error.message",
    "type": "$context.error.responseType",
    "is_expired": "$context.authorizer.booleanKey"
    }'''

# DEFAULT API GATEWAY RESPONSE BODY FOR 5XX STATUS CODE
RESPONSE_5XX = '''{"message": "Internal Server Error"}'''
