"""
This module defines the LayerStack
"""

from aws_cdk import core as cdk
from aws_cdk import aws_lambda as function
from aws_cdk import aws_cloudformation as cfn


class Layer(cfn.NestedStack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.utils_layer = function.LayerVersion(
            self,
            "CommonLayer",
            code=function.AssetCode("layers/common"),
            layer_version_name="new-common",
        )

        self.jwt_layer = function.LayerVersion(
            self,
            "JwtLayer",
            code=function.AssetCode("layers/jwt"),
            layer_version_name="new-jwt",
        )
