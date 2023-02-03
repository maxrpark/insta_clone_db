from rest_framework import permissions


class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(request.user and request.user.is_authenticated)


class IsUserObjectOrReadOnly(permissions.BasePermission):
    message = 'User is not a superuser'

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or bool(
            request.user == obj.author
        )
