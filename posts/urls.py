from django.urls import path
from .views import PostCreateView,LikeView, UnlikeView


urlpatterns = [
   path('create/', PostCreateView.as_view(), name='post_create'),
   path('like/<int:id>/', LikeView.as_view(), name='like'),
   path('unlike/<int:id>/', UnlikeView.as_view(), name='unlike'),
]