from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from ApiRequesters.Auth.permissions import IsAuthenticated, IsAppTokenCorrect
from ApiRequesters.Auth.AuthRequester import AuthRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError, UnexpectedResponse
from ApiRequesters.Awards.AwardsRequester import AwardsRequester
from ApiRequesters.Stats.decorators import collect_request_stats_decorator, CollectStatsMixin
from Users.models import Profile
from Users.serializers import ProfileSerializer, ProfilesListSerializer, SignUpSerializer
from Users.permissions import EditableByMeAndAdminPermission


class ProfilesListView(ListCreateAPIView, CollectStatsMixin):
    """
    Вьюха для спискового представления профилей
    """
    pagination_class = LimitOffsetPagination
    serializer_class = ProfilesListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Profile.objects.all()

    @collect_request_stats_decorator()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @collect_request_stats_decorator()
    def post(self, request, **kwargs):
        r = AuthRequester()
        token = get_token_from_request(request)
        try:
            auth_info = r.get_user_info(token)[1]
        except UnexpectedResponse as e:
            return Response(data=e.body, status=e.code)
        except BaseApiRequestError as e:
            return Response(data=str(e), status=500)

        data = request.data
        data['user_id'] = auth_info['id']
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProfileDetailView(RetrieveUpdateDestroyAPIView, CollectStatsMixin):
    """
    Вьюха для детального представления профиля
    """
    serializer_class = ProfileSerializer
    permission_classes = (EditableByMeAndAdminPermission, )
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return Profile.objects.all()

    @collect_request_stats_decorator()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @collect_request_stats_decorator()
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            response.status_code = 202
        return response


class AddNewAchievementView(APIView, CollectStatsMixin):
    """
    Вьюха для добавления нового пина
    """
    permission_classes = (IsAppTokenCorrect, )

    @collect_request_stats_decorator(another_stats_funcs=[CollectStatsMixin.collect_achievement_stats])
    def post(self, request: Request, user_id: int):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Такого пользователя не существует'}, status=404)

        try:
            achievement_id = request.data['achievement_id']
        except KeyError:
            return Response({'error': 'Необходимо указать achievement_id'}, status=400)

        if achievement_id in profile.get_achievements():
            return Response({'error': 'У пользователя уже есть это достижение'}, status=400)
        profile.add_achievement(achievement_id)
        s = ProfileSerializer(instance=profile)
        stats_kwargs = [{
            'achievement_id': achievement_id,
            'request': request,
        }]
        return Response(s.data, status=201), stats_kwargs


class BuyPinView(APIView, CollectStatsMixin):
    """
    Вьюха покупки пина
    """
    permission_classes = (IsAppTokenCorrect, )

    @collect_request_stats_decorator(another_stats_funcs=[CollectStatsMixin.collect_pin_purchase_stats])
    def post(self, request, user_id):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Такого пользователя не существует'}, status=404)

        try:
            pin_id = request.data['pin_id']
            price = request.data['price']
        except KeyError:
            return Response({'error': 'Необходимо указать id и price пина'}, status=400)

        if pin_id in profile.get_unlocked_pins():
            return Response({'error': 'У вас уже есть этот пин'}, status=400)
        if profile.money < price:
            return Response({'error': 'Недостаточно баллов для покупки'}, status=400)
        profile.add_pin(pin_id, price)
        s = ProfileSerializer(instance=profile)
        stats_kwargs = [{
            'pin_id': pin_id,
            'request': request,
        }]
        return Response(s.data, status=201), stats_kwargs


class ChangeRatingView(APIView, CollectStatsMixin):
    """
    Вьюха для изменения рейтинга
    """
    permission_classes = (IsAppTokenCorrect, )

    @collect_request_stats_decorator()
    def patch(self, request: Request, user_id: int):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Такого пользователя не существует'}, status=404)

        try:
            d_rating = request.data['d_rating']
        except KeyError:
            return Response({'error': 'Необходимо указать d_rating'}, status=400)

        profile.update_rating(d_rating)
        s = ProfileSerializer(instance=profile)
        return Response(s.data, status=202)


class SignUpView(APIView):
    """
    Вьюха для регистрации (с запросом на auth)
    """
    def post(self, request: Request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            _, tokens = AuthRequester().sign_up(request.data['username'], request.data['password'],
                                                request.data.get('email', ''))
            _, auth_json = AuthRequester().get_user_info(tokens['access'])
            profile = Profile.objects.create(user_id=auth_json['id'])
            profile_json = ProfileSerializer(instance=profile).data
            ret_data = {
                'token': tokens,
                'user': auth_json,
                'profile': profile_json,
            }
            return Response(ret_data, status=201)
        except (BaseApiRequestError, KeyError):
            return Response({'error': 'Error on creating new profile with user'}, status=400)
