"""
This module defines the LayerStack
"""

from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam


class BasicRole(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        managed_policy = [
            iam.ManagedPolicy.from_managed_policy_arn(
                self, "SMReadWrite", "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
            ),
            iam.ManagedPolicy.from_managed_policy_arn(
                self, "LambdaFullAccess", "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
            ),
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "AmazonSESFullAccess",
                "arn:aws:iam::aws:policy/AmazonSESFullAccess",
            ),
            iam.ManagedPolicy.from_managed_policy_arn(
                self, "AWSLambdaExecute", "arn:aws:iam::aws:policy/AWSLambdaExecute"
            ),
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "AWSLambdaBasicExecutionRole",
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
            ),
        ]

        self.basic_lambda_role = iam.Role(
            self,
            f"iamrole-{module_name}",
            role_name=f"iamrole-{module_name}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=managed_policy,
        )
