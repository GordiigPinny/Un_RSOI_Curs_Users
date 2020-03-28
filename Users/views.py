from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Response, Request
from django.contrib.auth.models import User
from Users.serializers import RegisterSerializer, UserSerializer, UserListSerializer


class RegisterView(APIView):
    """
    Вьюха для регистрации
    """
    def post(self, request: Request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    """
    Вьюха для спискового представления юзеров
    """
    pagination_class = LimitOffsetPagination
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.all()


class UserDetailView(APIView):
    """
    Вьюха для детального представления юзера
    """
    def get(self, request: Request, pk: int):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    """
    Вьюха для изменения пароля
    """
    def patch(self, request: Request, pk: int):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            old_password = request.data['old_password']
        except KeyError:
            return Response({'error': 'Не передан старый пароль'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_password = request.data['password']
        except KeyError:
            return Response({'error': 'Не передан новый пароль'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_password_confirm = request.data['password_confirm']
        except KeyError:
            return Response({'error': 'Не передано подтверждение нового пароля'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'error': 'Старый пароль не совпадает с текущим'}, status=status.HTTP_403_FORBIDDEN)
        if new_password != new_password_confirm:
            return Response({'error': 'Пароли не совпадают'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)