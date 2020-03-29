from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from Users.models import Profile
from Users.serializers import ProfileSerializer, ProfilesListSerializer


class ProfilesListView(ListCreateAPIView):
    """
    Вьюха для спискового представления профилей
    """
    pagination_class = LimitOffsetPagination
    serializer_class = ProfilesListSerializer

    def get_queryset(self):
        return Profile.objects.all()


class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    """
    Вьюха для детального представления профиля
    """
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        if response.status_code == 200:
            response.status_code = 202
        return response


class AddNewAwardView(APIView):
    """
    Вьюха для добавления нового пина
    """
    def post(self, request: Request, pk: int):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response(status=404)
        try:
            award_type, award_ids = request.data['award_type'], request.data['award_ids']
        except KeyError:
            return Response({'error': 'Необходимые поля: "award_type", "award_ids"'}, status=400)
        if not isinstance(award_ids, list):
            return Response({'error': '"award_ids" должен быть массивом'}, status=400)
        if len([x for x in award_ids if not isinstance(x, int)]) > 0:
            return Response({'error': '"award_ids" должен быть целочисленным массивом'}, status=400)
        if award_type == 'upin':
            profile.unlocked_geopins += ',' + ','.join([str(x) for x in award_ids])
        elif award_type == 'ppin':
            profile.unlocked_pins += ',' + ','.join([str(x) for x in award_ids])
        elif award_type == 'achievement':
            profile.achievements += ',' + ','.join([str(x) for x in award_ids])
        else:
            return Response({'error': 'Допустимые типы наград: "upin", "ppin", "achievement"'}, status=400)
        profile.save()
        s = ProfileSerializer(profile)
        return Response(s.data, status=201)
