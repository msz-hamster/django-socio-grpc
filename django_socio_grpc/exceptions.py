"""
Handled exceptions raised by socio grpc framework.

this file is almost identical to https://github.com/encode/django-rest-framework/blob/master/rest_framework/exceptions.py
But with the grpc code: https://grpc.github.io/grpc/python/grpc.html#grpc-status-code
This file will grown to support all the gRPC exception when needed
"""
from typing import Literal

from django.utils.translation import gettext_lazy as _
from grpc import StatusCode
from rest_framework import status
from rest_framework.exceptions import APIException


class ProtobufGenerationException(Exception):
    """
    Class for Socio gRPC framework protobuff generation exceptions.
    """

    default_detail = "Unknown"

    def __init__(self, app_name=None, model_name=None, detail=None):
        self.app_name = app_name
        self.model_name = model_name
        self.detail = detail if detail is not None else self.default_detail

    def __str__(self):
        return f"Error on protobuf generation on model {self.model_name} on app {self.app_name}: {self.detail}"


LOGGING_LEVEL = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class GRPCException(APIException):
    """
    Base class for Socio gRPC framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    You can also set `.logging_level` property to log the exception with the
    """

    status_code: StatusCode = StatusCode.INTERNAL
    logging_level: LOGGING_LEVEL = "WARNING"


class Unauthenticated(GRPCException):
    status_code = StatusCode.UNAUTHENTICATED
    default_detail = _("Authentication credentials were not provided.")
    default_code = "not_authenticated"


class PermissionDenied(GRPCException):
    status_code = StatusCode.PERMISSION_DENIED
    default_detail = _("You do not have permission to perform this action.")
    default_code = "permission_denied"


class NotFound(GRPCException):
    status_code = StatusCode.NOT_FOUND
    default_detail = _("Not found.")
    default_code = "not_found"


class AlreadyExist(GRPCException):
    status_code = StatusCode.ALREADY_EXISTS
    default_detail = _("Already exists.")
    default_code = "already_exist"


class InvalidArgument(GRPCException):
    status_code = StatusCode.INVALID_ARGUMENT
    default_detail = _("Invalid argument.")
    default_code = "invalid_argument"


class Unimplemented(GRPCException):
    status_code = StatusCode.UNIMPLEMENTED
    default_detail = _("Unimplemented.")
    default_code = "unimplemented"


HTTP_CODE_TO_GRPC_CODE = {
    status.HTTP_400_BAD_REQUEST: StatusCode.INVALID_ARGUMENT,
    status.HTTP_401_UNAUTHORIZED: StatusCode.UNAUTHENTICATED,
    status.HTTP_403_FORBIDDEN: StatusCode.PERMISSION_DENIED,
    status.HTTP_404_NOT_FOUND: StatusCode.NOT_FOUND,
    status.HTTP_405_METHOD_NOT_ALLOWED: StatusCode.UNIMPLEMENTED,
    status.HTTP_406_NOT_ACCEPTABLE: StatusCode.INVALID_ARGUMENT,
    status.HTTP_408_REQUEST_TIMEOUT: StatusCode.DEADLINE_EXCEEDED,
    status.HTTP_409_CONFLICT: StatusCode.ABORTED,
    status.HTTP_410_GONE: StatusCode.NOT_FOUND,
    status.HTTP_411_LENGTH_REQUIRED: StatusCode.INVALID_ARGUMENT,
    status.HTTP_412_PRECONDITION_FAILED: StatusCode.FAILED_PRECONDITION,
    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: StatusCode.INVALID_ARGUMENT,
    status.HTTP_414_REQUEST_URI_TOO_LONG: StatusCode.INVALID_ARGUMENT,
    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: StatusCode.INVALID_ARGUMENT,
    status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE: StatusCode.OUT_OF_RANGE,
    status.HTTP_417_EXPECTATION_FAILED: StatusCode.INVALID_ARGUMENT,
    status.HTTP_422_UNPROCESSABLE_ENTITY: StatusCode.INVALID_ARGUMENT,
    status.HTTP_423_LOCKED: StatusCode.FAILED_PRECONDITION,
    status.HTTP_424_FAILED_DEPENDENCY: StatusCode.FAILED_PRECONDITION,
    status.HTTP_428_PRECONDITION_REQUIRED: StatusCode.FAILED_PRECONDITION,
    status.HTTP_429_TOO_MANY_REQUESTS: StatusCode.RESOURCE_EXHAUSTED,
    status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE: StatusCode.INVALID_ARGUMENT,
    status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS: StatusCode.PERMISSION_DENIED,
    status.HTTP_500_INTERNAL_SERVER_ERROR: StatusCode.INTERNAL,
    status.HTTP_501_NOT_IMPLEMENTED: StatusCode.UNIMPLEMENTED,
    status.HTTP_502_BAD_GATEWAY: StatusCode.INTERNAL,
    status.HTTP_503_SERVICE_UNAVAILABLE: StatusCode.UNAVAILABLE,
    status.HTTP_504_GATEWAY_TIMEOUT: StatusCode.DEADLINE_EXCEEDED,
    status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED: StatusCode.UNIMPLEMENTED,
    status.HTTP_507_INSUFFICIENT_STORAGE: StatusCode.RESOURCE_EXHAUSTED,
    status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED: StatusCode.UNAUTHENTICATED,
}
