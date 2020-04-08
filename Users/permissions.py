from rest_framework.permissions import BasePermission
from ApiRequesters.Auth.AuthRequester import AuthRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError


class EditableByMeAndAdminPermission(BasePermission):
    """
    Пермишн на изменение инфы о юзере только самим юзером и админом
    """
    def has_permission(self, request, view):
        if request.methos == 'GET':
            return True
        requester = AuthRequester()
        try:
            _, auth_json = requester.get_user_info(get_token_from_request(requester))
        except BaseApiRequestError:
            return False
        return request.kwargs[view.lookup_url_kwarg] == auth_json['id'] or auth_json['is_superuser']
