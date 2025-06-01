from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.apps.baskets.models import Basket
from core.apps.baskets.serializers.api.basket import BasketListSerializer, BasketAddSerializer, BasketMergeSerializer

from core.apps.common.description import get_description


#TODO: переделать класс на кастомный из common
class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        #TODO: оптимизация + анотации
        user = self.request.user if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key
        qs = Basket.objects.for_user_or_session(user, session_key)
        return qs
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BasketAddSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key
        
        serializer.save(
            user=user,
            session_key=session_key
        )
    
    @action(detail=False, methods=['post'])
    def merge(self, request):
        """Слияние корзины из сессии с корзиной пользователя"""
        serializer = BasketMergeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'error': 'Пользователь не аутентифицирован'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        session_key = serializer.validated_data['session_key']
        
        # Переносим элементы корзины из сессии в пользователя
        Basket.objects.filter(
            session_key=session_key,
            user__isnull=True
        ).update(user=user, session_key='')
        
        return Response(
            {'message': 'Корзина успешно объединена'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Сводная информация о корзине"""
        queryset = self.get_queryset()
        total_sum = queryset.total_sum()
        total_quantity = queryset.total_quantity()
        
        return Response({
            'total_sum': total_sum,
            'total_quantity': total_quantity,
            'items': BasketListSerializer(queryset, many=True).data
        })
    
    @action(detail=True, methods=['delete'])
    def delete_item(self, request, pk=None):
        """Удаление товара из корзины"""
        try:
            basket = self.get_object()
            basket.delete()
            return Response({'message': 'Товар успешно удален из корзины'}, status=status.HTTP_200_OK)
        except Basket.DoesNotExist:
            return Response({'error': 'Товар не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)

backet_schema = extend_schema_view(
    list = extend_schema(
        summary = 'Получение списка товаров в корзине',
        description = 'Получение списка товаров в корзине',
        tags = ['baskets']
    ),
    create = extend_schema(
        summary = 'Добавление товара в корзину',
        description = 'Добавление товара в корзину',
        tags = ['baskets']
    ),
    summary = extend_schema(
        summary = 'Получение сводной информации о корзине',
        responses={
        200: OpenApiResponse(
            description='Успешный ответ с информацией о корзине',
            response={
                'type': 'object',
                'properties': {
                    'total_sum': {
                        'type': 'integer',
                        'description': 'Общая сумма товаров в корзине'
                    },
                    'total_quantity': {
                        'type': 'integer',
                        'description': 'Общее количество товаров в корзине'
                    },
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                # Описание полей вашего сериализатора BasketListSerializer
                            }
                        },
                        'description': 'Список товаров в корзине'
                    }
                }
            }
        ),
        400: OpenApiResponse(
            description='Ошибка валидации',
            response={
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Текст ошибки'
                    }
                }
            }
        )
    },
        description = 'Получение сводной информации о корзине',
        tags = ['baskets']
    ),
    merge = extend_schema(
        summary='Слияние корзины из сессии с корзиной пользователя',
    methods=['POST'],
    request=BasketMergeSerializer,
    responses={
        200: OpenApiResponse(
            description='Корзина успешно объединена',
            response={
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Сообщение об успешном объединении корзины'
                    }
                }
            }
        ),
        401: OpenApiResponse(
            description='Пользователь не аутентифицирован',
            response={
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Ошибка аутентификации'
                    }
                }
            }
        )
    },
    tags=['baskets']
    ),
    retrieve = extend_schema(
        summary = 'Получение информации о товаре в корзине',
        description = 'Получение информации о товаре в корзине',
        tags = ['baskets']
    ),
    delete_item = extend_schema(
        summary='Удаление товара из корзины',
    methods=['DELETE'],
    responses={
        200: OpenApiResponse(
            description='Товар успешно удален из корзины',
            response={
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Сообщение об успешном удалении товара'
                    }
                }
            }
        ),
        404: OpenApiResponse(
            description='Товар не найден в корзине',
            response={
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Ошибка, если товар не найден'
                    }
                }
            }
        )
    },
    tags=['baskets']
    ),
)

basket_schema = backet_schema(BasketViewSet)