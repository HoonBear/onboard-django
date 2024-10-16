import jwt

from typing import Optional
from django.utils import timezone
from jwt import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from django.conf import settings
from django.utils.encoding import smart_str
from rest_framework_simplejwt import authentication

from user.models import User


class JwtAuthentication(BaseAuthentication):

    @staticmethod
    def issue_token(identifier: int) -> str:
        # 현재 시간
        now = timezone.now()
        # 액세스 토큰의 만료 시간 설정 (30분 후)
        exp = now + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        # 사용자 식별자 클레임 설정
        user_id_claim = settings.SIMPLE_JWT["USER_ID_CLAIM"]

        return jwt.encode(
            payload={"iat": now, "exp": exp, user_id_claim: identifier},
            key=settings.SECRET_KEY,
            algorithm=settings.SIMPLE_JWT["ALGORITHM"],
        )

    @staticmethod
    def _parse_jwt_token_from_header(request: Request) -> Optional[str]:
        """Authorization 헤더에서 JWT 토큰을 파싱"""
        header_value = authentication.get_authorization_header(request)
        if not header_value:
            return None

        separated_auth_header_value = header_value.split()
        if len(separated_auth_header_value) != 2:
            raise exceptions.InvalidTokenError

        prefix, jwt_value = separated_auth_header_value

        auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()
        if smart_str(prefix.lower()) != auth_header_prefix:
            return None

        return jwt_value

    @staticmethod
    def _decode_jwt_token(token: str) -> dict:
        """JWT 토큰을 디코딩"""
        try:
            return jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=settings.SIMPLE_JWT["ALGORITHM"],
            )

        except jwt.ExpiredSignatureError as e:
            raise exceptions.InvalidTokenError
        except jwt.DecodeError as e:
            raise exceptions.InvalidTokenError
        except jwt.InvalidTokenError as e:
            raise exceptions.InvalidTokenError

    def authenticate(self, request):

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # 인증 정보가 없는 경우

        try:
            # 'Bearer <token>' 형식에서 토큰 추출
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None

            # 토큰 검증
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
            )

            # 사용자 객체 가져오기
            user_id = payload.get(settings.SIMPLE_JWT["USER_ID_CLAIM"])
            user = User.objects.get(id=user_id)

        except (ValueError, jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token or user not found.')

        return (user, token)  # (사용자, 토큰) 반환