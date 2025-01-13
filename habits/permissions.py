from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только владелец объекта может редактировать или удалять.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем только просмотр (GET, HEAD, OPTIONS) для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Редактирование и удаление разрешено только владельцу (поле user)
        return obj.user == request.user
