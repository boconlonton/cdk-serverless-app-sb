"""
This module defines the default template for API Gateway respons
"""

# GENERAL SETTINGS
AWS_REGION_NAME = 'us-east-1'
CDK_ELEMENT_PREFIX = 'dev'

# DEFAULT API GATEWAY RESPONSE HEADER
HEADER = {
    'Access-Control-Allow-Headers': "'*'",
    'Access-Control-Allow-Methods': "'*'",
    'Access-Control-Allow-Origin': "'*'",
}

# DEFAULT API GATEWAY RESPONSE BODY FOR 4XX STATUS CODE
RESPONSE_4XX = '''{
    "message": "$context.error.message",
    "is_expired": "$context.authorizer.booleanKey"
    }'''

# DEFAULT API GATEWAY RESPONSE BODY FOR 5XX STATUS CODE
RESPONSE_5XX = '''{"message": "Internal Server Error"}'''

# SETTINGS FOR AWS SECRET MANAGER
SECRET_ARN = 'arn:aws:acm:us-east-1:573915606947:sm/5a4c6547-41b7-4f2e-8ab2-4cef78d693a8'

# SETTINGS FOR AWS AURORA
RESOURCE_ARN = 'arn:aws:acm:us-east-1:573915606947:aurora/5a4c6547-41b7-4f2e-8ab2-4cef78d693a8'
