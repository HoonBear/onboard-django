from rest_framework import status
from rest_framework.exceptions import APIException


class ServerApiException(APIException):
    default_detail = "unexpected server error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

class AuthorizationException(APIException):
    default_detail = "request has no authority"
    status_code = status.HTTP_403_FORBIDDEN

class DuplicatedUserLoginIdException(ServerApiException):
    default_detail = "duplicated user loginId"
    status_code = status.HTTP_400_BAD_REQUEST

class IdOrPasswordNotFoundException(ServerApiException):
    default_detail = "invalid id or password"
    status_code = status.HTTP_401_UNAUTHORIZED

class DuplicatedDibsGroupNameException(ServerApiException):
    default_detail = "duplicated dibs group name"
    status_code = status.HTTP_400_BAD_REQUEST

class DuplicatedDibsProduct(ServerApiException):
    default_detail = "duplicated dibs product"
    status_code = status.HTTP_400_BAD_REQUEST
