"""
This module defines the endpoint configuration for all users api endpoint.
These configuration includes:
- endpoint sub-path
- endpoint path parameter
- additional environment for handler of each endpoint
"""

url = {
    'get-all': {
        'method': 'GET',
        'environment': {
            'resource-arn': 'abc'
        }
    },
    'get': {
        'method': 'GET',
        'pathParams': '{user_id}',
        'environment': {
            'resource-arn': 'abc',
        },
    },
    'create': {
        'method': 'POST',
    },
    'update': {
        'method': 'GET'
    }
}
