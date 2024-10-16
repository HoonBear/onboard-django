from rest_framework.views import exception_handler


def server_exception_handler(exc, context):
    response = exception_handler(exc, context)

    try:
        if response is None:
            return None
        response.data["message"] = response.data.pop("detail")
    except KeyError:
        # NOTE: detail이 없는 예외 (시리얼라이저의 ValidationError 등)은 일단 내려보냄
        return response
    except TypeError:
        # NOTE: Validation을 List로 받는 경우 발생
        return response

    return response
