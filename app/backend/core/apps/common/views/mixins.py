from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from core.apps.common.constants import roles

class ExtendedView():
    multi_permission_classes = None
    multi_serializer_classes = None
    request = None

    def get_serializer_class(self):
        assert self.serializer_class or self.multi_serializer_classes, (
            "'%s' should either include a `serializer_class`, "
            "multi_serializer_classes, attribute, or override"
            " the `get_serializer_class()` method." % self.__class__.__name__
        )

        if not self.multi_serializer_classes:
            return self.serializer_class

        user = self.request.user
        if user.is_anonymous:
            user_roles = (roles.PUBLIC_GROUP,)
        elif user.is_superuser:
            user_roles = (roles.ADMIN_GROUP,)
        else:
            user_roles = set(user.groups.all().values_list('code', flat=True))

        if hasattr(self, 'action') and self.action:
            action = self.action
        else:
            action = self.request.method

        for role in user_roles:
            serializer_key = f"{role}_{action}"
            if self.multi_serializer_classes.get(serializer_key):
                return self.multi_serializer_classes.get(serializer_key)
        
        for role in user_roles:
            serializer_key = f"{role}"
            if self.multi_serializer_classes.get(serializer_key):
                return self.multi_serializer_classes.get(serializer_key)

        return self.multi_serializer_classes.get(action) or self.serializer_class
    
    def get_permissions(self):
        if hasattr(self, 'action') and self.action:
            action = self.action
        else:
            action = self.request.method

        if self.multi_permission_classes:
            permissions = self.multi_permission_classes.get(action)
            if permissions:
                return [permission() for permission in permissions]

        return [permission() for permission in self.permission_classes]

        

class ExtendedGenericViewSet(ExtendedView, GenericViewSet):
    pass

class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    pass

class CRUViewSet(ExtendedGenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    pass

class CRUDViewSet(CRUViewSet,
                  mixins.DestroyModelMixin):
    pass

class CDViewSet(ExtendedGenericViewSet,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin):
    pass