#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from cdk.layer_stack import Layer
from cdk.basic_role_stack import BasicRole
from cdk.lib.construct import Authorizer


app = cdk.App()

init_stack = cdk.Stack(app, 'init')
layer = Layer(init_stack, 'layers')
basic_role = BasicRole(init_stack, 'roles')

authorizer_stack = cdk.Stack(app, 'authorizer')
fn_auth = Authorizer(
    authorizer_stack,
    f'authorizer-id',
    env={'abcd': 'def'},
    layers=[layer.jwt_layer],
    role=basic_role.basic_lambda_role
)

app.synth()
