from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Настройка прав доступа для каждого действия"""
        if self.action == "create":
            permission_classes = []
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def _check_ownership(self, obj):
        """Проверка: пользователь может редактировать только себя"""
        if obj.id != self.request.user.id and not self.request.user.is_staff:
            return Response({"error": "Вы можете редактировать только свой профиль"}, status=status.HTTP_403_FORBIDDEN)
        return None

    def update(self, request, *args, **kwargs):
        """Пользователь может редактировать только себя"""
        obj = self.get_object()
        error_response = self._check_ownership(obj)
        if error_response:
            return error_response
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Пользователь может редактировать только себя"""
        obj = self.get_object()
        error_response = self._check_ownership(obj)
        if error_response:
            return error_response
        return super().partial_update(request, *args, **kwargs)
