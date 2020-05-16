from rest_framework.permissions import BasePermission
from ApiRequesters.Auth.AuthRequester import AuthRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError
from Users.models import Profile


class EditableByMeAndAdminPermission(BasePermission):
    """
    Пермишн на изменение инфы о юзере только самим юзером и админом
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        r = AuthRequester()
        try:
            _, auth_json = r.get_user_info(get_token_from_request(request))
        except BaseApiRequestError:
            return False
        return int(view.kwargs[view.lookup_url_kwarg]) == auth_json['id'] or auth_json['is_superuser']
