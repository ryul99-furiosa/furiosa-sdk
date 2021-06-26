"""
    Furiosa AI Web Service API

    Furiosa AI Web Service API for Compiler and Model Tools  # noqa: E501

    The version of the OpenAPI document: v1alpha
    Contact: contact@furiosa.ai
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from furiosa.openapi.api_client import ApiClient, Endpoint as _Endpoint
from furiosa.openapi.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types,
)
from furiosa.openapi.model.api_response import ApiResponse


class PerfeyeApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __api_profiler_v1alpha1_perfeye_post(self, x_request_id, source, **kwargs):
            """Generate a visualized performance estimation  # noqa: E501

            It will generate a single HTML containing a DAG with estimated performance results  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.api_profiler_v1alpha1_perfeye_post(x_request_id, source, async_req=True)
            >>> result = thread.get()

            Args:
                x_request_id (str):
                source (file_type): a byte array of a source image

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                str
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs["async_req"] = kwargs.get("async_req", False)
            kwargs["_return_http_data_only"] = kwargs.get("_return_http_data_only", True)
            kwargs["_preload_content"] = kwargs.get("_preload_content", True)
            kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
            kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
            kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
            kwargs["_host_index"] = kwargs.get("_host_index")
            kwargs["x_request_id"] = x_request_id
            kwargs["source"] = source
            return self.call_with_http_info(**kwargs)

        self.api_profiler_v1alpha1_perfeye_post = _Endpoint(
            settings={
                "response_type": (str,),
                "auth": ["AccessKeyIdAuth", "SecretAccessKeyAuth"],
                "endpoint_path": "/api/profiler/v1alpha1/perfeye",
                "operation_id": "api_profiler_v1alpha1_perfeye_post",
                "http_method": "POST",
                "servers": None,
            },
            params_map={
                "all": [
                    "x_request_id",
                    "source",
                ],
                "required": [
                    "x_request_id",
                    "source",
                ],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "x_request_id": (str,),
                    "source": (file_type,),
                },
                "attribute_map": {
                    "x_request_id": "X-Request-ID",
                    "source": "source",
                },
                "location_map": {
                    "x_request_id": "header",
                    "source": "form",
                },
                "collection_format_map": {},
            },
            headers_map={
                "accept": ["text/html", "application/json"],
                "content_type": ["multipart/form-data"],
            },
            api_client=api_client,
            callable=__api_profiler_v1alpha1_perfeye_post,
        )
