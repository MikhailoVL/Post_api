from django.urls import path

from .api_views import PostListAPIView, UserSignUpAPIView, CreateTokenView,\
    PostCreateAPIView, LikeUnlikeCreateAPIView, UsersListAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='posts'),
    path('posts/create/', PostCreateAPIView.as_view(), name='create'),
    path('users/sign_up/', UserSignUpAPIView.as_view(), name='users/sign_up'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('like_unlike/', LikeUnlikeCreateAPIView.as_view(), name='like_unlike'),
    path('users/', UsersListAPIView.as_view(), name="users")

]
