from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

class ExtendedGenericViewSet(GenericViewSet):
    pass

class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    pass

class CRUViewSet(ExtendedGenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    pass

class CRUDViewSet(ExtendedGenericViewSet,
                  mixins.DestroyModelMixin):
    pass