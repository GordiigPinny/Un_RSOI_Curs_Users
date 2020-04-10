import json
from ApiRequesters.Mock.MockRequesterMixin import MockRequesterMixin


class TestToken:
    """
    Базовый класс для токена, использующегося в тестах
    Представляет собой просто строку -- настоящий токен
    """
    def __init__(self, token, prefix: str = 'Bearer'):
        self.prefix = prefix
        self._token = token

    @property
    def token(self):
        return self.prefix + ' ' + self._token

    def set_error(self, service: MockRequesterMixin.ERRORS_KEYS, error: MockRequesterMixin.ERRORS):
        pass

    def set_role(self, role: MockRequesterMixin.ROLES):
        pass

    def set_another_key(self, key: str, val: str):
        pass


class TestMockToken(TestToken):
    """
    Токен для мок-тестов
    Токен -- словарь, подходящий к мок-тестам
    """
    def __init__(self, token=None):
        super().__init__(token={'role': 'USER'})

    @property
    def token(self):
        return json.dumps(self._token)

    def set_error(self, service: MockRequesterMixin.ERRORS_KEYS, error: MockRequesterMixin.ERRORS):
        self._token[service] = error

    def set_role(self, role: MockRequesterMixin.ROLES):
        self._token['role'] = role

    def set_another_key(self, key: str, val: str):
        self._token[key] = val
