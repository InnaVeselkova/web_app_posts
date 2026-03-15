from rest_framework import viewsets, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import (
    PostSerializer, PostCreateSerializer,
    CommentSerializer, CommentCreateSerializer
)
from rest_framework.permissions import IsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с постами.
    """

    queryset = Post.objects.select_related('author').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """При создании поста автором становится текущий пользователь"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """При обновлении проверяем, что пользователь - автор"""
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied("Вы можете редактировать только свои посты.")
        serializer.save()

    def perform_destroy(self, instance):
        """При удалении проверяем, что пользователь - автор"""
        if instance.author != self.request.user:
            raise exceptions.PermissionDenied("Вы можете удалять только свои посты.")
        instance.delete()

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Получить все комментарии к посту"""
        post = self.get_object()
        comments = post.comments.select_related('author').all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.
    """

    queryset = Comment.objects.select_related('author', 'post').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        """При создании комментария автором становится текущий пользователь"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """При обновлении проверяем, что пользователь - автор"""
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied("Вы можете редактировать только свои комментарии.")
        serializer.save()

    def perform_destroy(self, instance):
        """При удалении проверяем, что пользователь - автор"""
        if instance.author != self.request.user:
            raise exceptions.PermissionDenied("Вы можете удалять только свои комментарии.")
        instance.delete()
