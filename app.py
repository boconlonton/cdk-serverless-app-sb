#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from cdk.layer_stack import Layer
from cdk.basic_role_stack import BasicRole
from cdk.lib.construct import Authorizer
from cdk.lib.construct import API

from lambdas.users.views import url as user_views

app = cdk.App()

# Base stack
init_stack = cdk.Stack(app, 'init')
layer = Layer(init_stack, 'layers')
basic_role = BasicRole(init_stack, 'roles')

# Authorizer stack
fn_auth = Authorizer(
    cdk.Stack(app, 'authorizer'),
    f'authorizer-id',
    env={'abcd': 'def'},
    layers=[layer.jwt_layer],
    role=basic_role.basic_lambda_role,
)

# User APIs
users_api = API(cdk.Stack(app, 'users'),
                construct_id=f'users-apis',
                stage=os.getenv('ENV', 'dev'),
                module_name='user',
                layers=[layer.jwt_layer, layer.utils_layer],
                role=basic_role.basic_lambda_role,
                env={},
                views=user_views,
                authorizer=fn_auth.handler)
users_api()

app.synth()
