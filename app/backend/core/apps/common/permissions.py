from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение только для админа  или чтение"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'
    

class IsAdmin(permissions.BasePermission):
    """Только авторизованный user c ролью admin"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)