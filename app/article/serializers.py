import json

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Post, Likes


class UserListSerializer(serializers.Serializer):
    """Serializer for user list last_login"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    last_login = serializers.DateTimeField(required=True)
    class meta:
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    """Serializer for create"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True,
                                     style={'input_type': 'password',
                                            'placeholder': 'Password'},
                                     trim_whitespace=False,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True,
                                      style={'input_type': 'password',
                                             'placeholder': 'Password'
                                             },
                                      trim_whitespace=False,
                                      required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'first_name',
            'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PostCreateSerializer(serializers.Serializer):
    """Serializer for post create"""
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    body = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ['title', 'description', 'body']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Post.objects.create(**validated_data)


class LikeUnLikeSerializer(serializers.Serializer):
    """Serializer for like"""
    is_fan = serializers.BooleanField(required=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class meta():
        fields = ['is_fan', 'post']

    def create(self, validated_data):
        post_id = validated_data.get('post').id
        # All users that like the post
        user_liked = [like.user for like in Likes.objects.filter(post=post_id)]
        user = self.context['request'].user
        validated_data['user'] = user
        curent_like = Likes.objects.filter(post=post_id, User=user)

        if user in user_liked:
            # user remove his like
            if validated_data['is_fan'] == curent_like[0].is_fan:
                curent_like.delete()
            else:
                # if user change minded
                Likes.objects.update(**validated_data)
            return validated_data

        return Likes.objects.create(**validated_data)


class PostSerializer(serializers.Serializer):
    """Serializer for the post """
    id = serializers.IntegerField(required=True)
    autor = serializers.CharField(source='user.email')
    title = serializers.CharField(required=True)

    total_likes = serializers.SerializerMethodField(
        method_name='get_total_likes', read_only=True)
    is_like = serializers.SerializerMethodField(
        method_name='get_total_is_like', read_only=True
    )
    is_hater = serializers.SerializerMethodField(
        method_name='get_total_hater', read_only=True
    )

    class Meta:
        model = Post
        fields = [
            'id', 'autor', 'title', 'total_likes', 'is_like', 'is_hater'
        ]

    def get_total_likes(self, post):
        likes = Likes.objects.all()
        return likes.filter(post=post.id).count()

    def get_total_is_like(self, post):
        likes = Likes.objects.all()
        return likes.filter(post=post.id, is_fan=True).count()

    def get_total_hater(self, post):
        likes = Likes.objects.all()
        return likes.filter(post=post.id, is_fan=False).count()


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,
                                     style={'input_type': 'password'},
                                     trim_whitespace=False
                                     )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')

        attrs['user'] = user
        return attrs
