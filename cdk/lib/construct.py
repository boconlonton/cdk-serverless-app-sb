"""
This module defines the base class for:
- APIGateway
- Authorizer
- APIHandler
"""
from typing import List, Mapping

from aws_cdk import core as cdk
from aws_cdk import aws_lambda as function
from aws_cdk import aws_apigateway as api
from aws_cdk import aws_iam as iam

from settings.dev import HEADER
from settings.dev import RESPONSE_4XX
from settings.dev import RESPONSE_5XX


class Authorizer(cdk.Construct):
    """
    This class defines CDK Construct for a Lambda-authorizer
    """

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 *,
                 module_name: str,
                 env: Mapping[str, str],
                 layers: List[function.LayerVersion],
                 role: iam.Role,
                 timeout: cdk.Duration = cdk.Duration.seconds(10),
                 handler: str = 'authorizer.handler',
                 runtime: function.Runtime = function.Runtime.PYTHON_3_7(),
                 code: function.Code = function.Code.asset('lambdas/authorizer'),
                 ):
        """

        Args:
            scope (Stack): specify which stack this resource belongs to
            construct_id (str): the unique id for the resource
            module_name (str): specify which module this resource belong to
            env (dict): specify the environment for this AWS Lambda function
            layers (list): specify the
            role:
            timeout:
            handler:
            runtime:
            code:
        """
        super().__init__(scope, construct_id)

        self.handler = function.Function(
            self,
            id=construct_id,
            function_name=f'{module_name}-authorizer',
            runtime=runtime,
            code=code,
            handler=handler,
            role=role,
            layers=layers,
            timeout=timeout,
            environment=env
        )


class Handler(cdk.Construct):
    """
    This class defines CDK Construct for a Lambda-authorizer
    """

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 *,
                 module_name: str,
                 fn_name: str,
                 env: Mapping[str, str],
                 layers: List[function.LayerVersion],
                 role: iam.Role,
                 code_location: str,
                 timeout: cdk.Duration = cdk.Duration.seconds(10),
                 handler: str = 'authorizer.handler',
                 runtime: function.Runtime = function.Runtime.PYTHON_3_7,
                 ):
        """

        Args:
            scope (Stack): specify which stack this resource belongs to
            construct_id (str): the unique id for the resource
            module_name (str): specify which module this resource belong to
            fn_name (str): specify the file name of the handler
            env (dict): specify the environment for this AWS Lambda function
            layers (list): specify the
            role:
            timeout:
            handler:
            runtime:
            code:
        """
        super().__init__(scope, construct_id)

        self.handler = function.Function(
            self,
            id=construct_id,
            function_name=f'{module_name}-{fn_name}',
            runtime=runtime,
            code=function.Code.asset(code_location),
            handler=handler,
            role=role,
            layers=layers,
            timeout=timeout,
            environment=env
        )


class API(cdk.Construct):
    """
    This class defines an API instance
    """

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 *,
                 stage: str,
                 module_name: str,
                 layers: List[function.LayerVersion],
                 role: iam.Role,
                 env: dict,
                 authorizer: function.Function = None,
                 endpoint_types: List[api.EndpointType] = api.EndpointType.REGIONAL,
                 headers: Mapping[str, str] = HEADER,
                 template_4xx: str = RESPONSE_4XX,
                 template_5xx: str = RESPONSE_5XX,
                 ):
        """

        Args:
            scope:
            construct_id:
            stage:
            module_name:
            layers:
            role:
            authorizer:
            endpoint_types:
            headers:
            template_4xx:
            template_5xx:
        """
        super().__init__(scope, construct_id)

        self._module_name = module_name
        self._layers = layers
        self._role = role
        self._env = env

        self.root_node = api.RestApi(
            self,
            id=f'{stage}.api.{module_name}',
            endpoint_types=endpoint_types,
            deploy=True,
        )

        # GATEWAY RESPONSE
        self.root_node.add_gateway_response(
            id=f'{module_name}-response-4xx',
            type=api.ResponseType.DEFAULT_4_XX(),
            response_headers=headers,
            status_code="400",
            templates={"application/json": template_4xx},
        )

        self.root_node.add_gateway_response(
            id=f"{module_name}-default-5xx",
            type=api.ResponseType.DEFAULT_5_XX(),
            response_headers=headers,
            status_code="500",
            templates={"application/json": template_5xx},
        )

        # CUSTOM AUTHORIZER
        if authorizer:
            self._api_auth = api.RequestAuthorizer(
                self,
                id=f"{module_name}-api-authorizer",
                authorizer_name=f"{module_name}-authorizer",
                handler=authorizer,
                results_cache_ttl=cdk.Duration.minutes(0),
                identity_sources=[api.IdentitySource.header("Authorization")],
            )

        # ENABLE CORS
        cors = function.Function(
            self,
            id=f'{module_name}-cors',
            function_name=f"{module_name}-cors",
            runtime=function.Runtime.PYTHON_3_7(),
            code=function.Code.asset("functions/cors"),
            handler="cors.handler",
        )

        # DEPLOY & STAGE
        deployment = api.Deployment(
            self,
            f'{module_name}-deployment',
            api=self.root_node,
            retain_deployments=False,
        )

        stage = api.Stage(
            self,
            f"{module_name}-stage-{stage}",
            deployment=deployment,
            stage_name=f'{module_name}-{stage}',
            variables={"schema": stage, "alias": stage},
        )

        self.root_node.deployment_stage = stage

        # DOMAIN & MAPPING
        domain = api.DomainName.from_domain_name_attributes(
            self,
            id=f'{module_name}-domain',
            domain_name=DOMAIN_NAME,
            domain_name_alias_hosted_zone_id=HOSTED_ZONE,
            domain_name_alias_target=APIGW_DOMAIN_NAME,
        )

        mapping = api.CfnBasePathMapping(
            self,
            id=f'{module_name}-mapping',
            domain_name=domain.domain_name,
            rest_api_id=self.root_node.rest_api_id,
            base_path=f"{module_name}",
            stage=stage.stage_name,
        )

    def __call__(self, *, data, **kwargs):
        """

        Args:
            data:
            **kwargs:

        Returns:

        """
        # MODULE CODE
        root_directory = f'lambdas/{self._module_name}'

        # LOOP TO PROVISION LAMBDA FUNCTIONS OF MODULE
        for endpoint, metadata in data.items():

            path = f'{root_directory}/{endpoint}'

            # UPDATE LAMBDA FUNCTION ENVIRONMENT
            if kwargs.get(endpoint):
                self._env.update(kwargs[endpoint])
            if metadata.get('environment'):
                self._env.update(metadata['environment'])

            # DECLARE LAMBDA FUNCTION
            handler = Handler(
                self,
                construct_id=f'{self._module_name}-{endpoint}',
                module_name=self._module_name,
                fn_name=endpoint,
                env=self._env,
                layers=self._layers,
                role=self._role,
                code_location=path
            )

            # ENDPOINT
            child_node = self.root_node.root.add_resource(endpoint)

            if metadata.get('pathParams'):
                # ENDPOINT HAS PATH-PARAM
                api_endpoint = child_node.add_resource(metadata['pathParams'])
            else:
                # ENDPOINT HAS NO PATH-PARAMS
                api_endpoint = child_node

            api_endpoint.add_method(
                http_method=metadata.get('method'),
                integration=api.LambdaIntegration(handler),
                authorizer=self._api_auth,
            )

            # ENABLE CORS
            api_endpoint.add_method(
                http_method='OPTIONS',
                integration=api.LambdaIntegration(self.cors)
            )
