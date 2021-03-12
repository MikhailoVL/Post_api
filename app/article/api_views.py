from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django_filters import rest_framework as filters

from .utils_filter import DateRangeFilter
from .serializers import PostSerializer, UserSerializer, AuthTokenSerializer,\
    PostCreateSerializer, LikeUnLikeSerializer, UserListSerializer

from .models import Post, Likes
from django.contrib.auth.models import User


class PostListAPIView(ListAPIView):
    """All post , all likes, likes, dislike"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DateRangeFilter


class PostCreateAPIView(CreateAPIView):
    """Create new Post"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class UserSignUpAPIView(CreateAPIView):
    """Register new user"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UsersListAPIView(ListAPIView):
    """Show all user last login """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class LikeUnlikeCreateAPIView(CreateAPIView):
    """Create new like"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = Likes.objects.all()
    serializer_class = LikeUnLikeSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
