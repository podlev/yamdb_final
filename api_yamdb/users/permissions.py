from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Права доступа администратор"""

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """Права доступа администратор или только для чтения"""

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin)):
            return True
        return False


class IsReadOnlyOrIsAuthorOrIsModerator(BasePermission):
    """Права доступа администратор, модератор, автор или только для чтения"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user):
            return True
        else:
            return False
