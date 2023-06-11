from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # auth
    path('login/', views.LoginView.as_view(), name='sign_in'),
    path('registration/', views.UserRegisterView.as_view(), name='register'),
    path('sign_out/', views.logout_user, name='sign_out'),
    
    # user password reset paths
    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/auth/password_reset_done.html"),
         name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/auth/password_reset_confirm.html"),
         name="password_reset_confirm"
         ),
    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/auth/password_reset_complete.html"),
         name="password_reset_complete"
         ),
    
    path("user/password/reset/", views.password_reset, name="password_reset"),
    
    # user account
    path('<int:pk>/', views.UserAccDetailView.as_view(), name='user_acc'),
    path('<int:pk>/post-archive/', views.UserPostsListView.as_view(), name='post_archive'),
    path('profile/', views.UpdateUserProfileView.as_view(), name='user_profile'),
    path('search/', views.UsersSearchListView.as_view(), name='users_search'),
    path('<int:user_pk>/following/', views.FollowingListView.as_view(), name='following'),
    path('<int:user_pk>/followers/', views.FollowersListView.as_view(), name='followers'),
    
    # follows
    path('follow/<int:user_pk>/', views.FollowUser.as_view(), name='follow_user'),
    path('unfollow/<int:user_pk>/', views.UnfollowUser.as_view(), name='unfollow_user'),

]
