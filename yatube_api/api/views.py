from django.shortcuts import get_object_or_404
from rest_framework import (filters,
                            viewsets,
                            permissions,
                            )
from rest_framework.pagination import LimitOffsetPagination

from api import serializers
from api.permissions import IsAuthorOrReadOnly
from posts import models


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки постов."""
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки групп."""
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки комментариев."""
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        return get_object_or_404(models.Post, pk=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки подписок."""
    serializer_class = serializers.FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return models.Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
