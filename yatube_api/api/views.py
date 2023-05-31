from django.shortcuts import get_object_or_404
from rest_framework import (filters,
                            viewsets,
                            permissions,
                            )
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer,
                             FollowSerializer,
                             GroupSerializer,
                             PostSerializer,
                             )
from posts.models import (Follow,
                          Group,
                          Post,
                          )


class PostViewSet(viewsets.ModelViewSet):
    '''Вьюсет для обработки постов.'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            msg = 'У вас недостаточно прав для выполнения данного действия.'
            raise PermissionDenied(msg)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            msg = 'У вас недостаточно прав для выполнения данного действия.'
            raise PermissionDenied(msg)
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет для обработки групп.'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для обработки комментариев.'''
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    '''Вьюсет для обработки подписок.'''
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
