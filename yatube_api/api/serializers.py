from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CurrentUserDefault

from posts import models


class PostSerializer(serializers.ModelSerializer):
    '''Серилизатор постов. '''
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              )

    class Meta:
        model = models.Post
        fields = (
            'id', 'text', 'author', 'image', 'group', 'pub_date', 'comments'
        )
        read_only_fields = ('comments',)


class CommentSerializer(serializers.ModelSerializer):
    '''Серилизатор комментариев. '''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'created', 'post')
        read_only_fields = ('id', 'author', 'created', 'post')


class GroupSerializer(serializers.ModelSerializer):
    '''Серилизатор групп. '''

    class Meta:
        model = models.Group
        fields = ('id', 'title', 'slug', 'description')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'password')


class FollowSerializer(serializers.ModelSerializer):
    '''Серилизатор подписок. '''
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=models.User.objects.all(),
    )

    class Meta:
        model = models.Follow
        fields = ('id', 'user', 'following')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=models.Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на данного автора!',
            ),
        )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Вы не можете подписаться сам на себя!'
            )
        return data
