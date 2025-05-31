from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.apps.users.serializers.api import user as user_serializers

User = get_user_model()


#TODO наследоватся от кастомного представления из common
@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        description='Регистрация пользователя',
        tags=['auth'],
        # request=RegistrationSerializer,
        # responses={201: RegistrationSerializer}
    )
)
class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializers.RegistrationSerializer
    permission_classes = (AllowAny,)

#TODO наследоватся от кастомного представления из common
@extend_schema_view(
    post=extend_schema(
        summary='Смена пароля',
        description='Смена пароля',
        tags=['auth'],
        request=user_serializers.ChangePasswordSerializer,
        responses={204: user_serializers.ChangePasswordSerializer}
    )
)
class ChangePasswordView(APIView):
    
    def post(self, request):
        user = request.user
        serializer = user_serializers.ChangePasswordSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#TODO наследоватся от кастомного представления из common
@extend_schema_view(
    get=extend_schema(
        summary='Получение информации о пользователе',
        description='Получение информации о пользователе',
        tags=['auth'],
        responses={200: user_serializers.MeSerializer}
    ),
    put=extend_schema(
        summary='Обновление информации о пользователе',
        description='Обновление информации о пользователе',
        tags=['auth'],
        request=user_serializers.MeUpdateSerializer,
        responses={200: user_serializers.MeUpdateSerializer}
    ),
    patch=extend_schema(
        summary='Частичное обновление информации',
        description='Частичное обновление информации о пользователе',
        tags=['auth'],
        request=user_serializers.MeUpdateSerializer,
        responses={200: user_serializers.MeUpdateSerializer}
    )
)
class MeView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializers.MeSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch']

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return user_serializers.MeUpdateSerializer
        if self.request.method == 'GET':
            return user_serializers.MeSerializer
        return self.serializer_class
    
    def get_object(self):
        return self.request.user