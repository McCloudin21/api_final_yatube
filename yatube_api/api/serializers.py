from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CurrentUserDefault


from posts.models import (Comment,
                          Group,
                          Follow,
                          Post,
                          User,
                          )


class PostSerializer(serializers.ModelSerializer):
    '''Серилизатор постов. '''
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              )

    class Meta:
        model = Post
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
        model = Comment
        fields = ('id', 'text', 'author', 'created', 'post')
        read_only_fields = ('id', 'author', 'created', 'post')


class GroupSerializer(serializers.ModelSerializer):
    '''Серилизатор групп. '''

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
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
