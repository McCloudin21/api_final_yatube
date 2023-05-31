from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()

router.register(r'^posts', views.PostViewSet, basename='post')
router.register(r'^groups', views.GroupViewSet, basename='group')
router.register(
    r'^posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet, basename='comment'
)
router.register(r'^follow', views.FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
