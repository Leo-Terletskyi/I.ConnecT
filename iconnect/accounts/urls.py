from django.urls import path

from . import views


urlpatterns = [
    # auth
    path('login/', views.LoginView.as_view(), name='sign_in'),
    path('registration/', views.UserRegisterView.as_view(), name='register'),
    path('sign_out/', views.logout_user, name='sign_out'),
    
    # user account
    path('<int:pk>/', views.UserAccDetailView.as_view(), name='user_acc'),
    path('<int:pk>/post-archive/', views.UserPostsListView.as_view(), name='post_archive'),
    path('profile/', views.UpdateUserProfileView.as_view(), name='user_profile'),
    
]
