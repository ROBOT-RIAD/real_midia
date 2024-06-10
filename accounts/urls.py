from django.urls import path
from .views import UserSignupView,UserLoginView,EditProfileView,ProfileView,UserProfileView,LogoutView,FollowView, UnFollowView, Activate



urlpatterns = [
    path("signup/",UserSignupView.as_view(),name ='signup'),
    path("login/",UserLoginView.as_view(),name ='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit-bio/', EditProfileView.as_view(), name='edit_bio'), 
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('follow/<int:id>/', FollowView.as_view(), name='follow_user'),
    path('unfollow/<int:id>/', UnFollowView.as_view(), name='unfollow_user'),
    path('active/<uid64>/<token>/', Activate,name ='activate'),
]