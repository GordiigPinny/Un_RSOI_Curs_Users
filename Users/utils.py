from typing import Union
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


def get_token_from_header(request) -> Union[str, None]:
    """
    Получаем токен из header'а запроса
    """
    try:
        return request.META.get['HTTP_AUTHORIZATION'][7:]
    except KeyError:
        return None


def get_user_from_token(token: str) -> Union[User, None]:
    """
    Получаем юзера из ДЖВТ-токена
    """
    try:
        return VerifyJSONWebTokenSerializer().validate({'token': token})
    except ValidationError:
        return None
