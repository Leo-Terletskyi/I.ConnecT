from django.urls import path

from . import views

urlpatterns = [
    path('new-post/', views.PostCreateView.as_view(), name='create_post'),
    path('update-post/<int:post_pk>/', views.PostUpdateView.as_view(), name='update_post'),
    path('archiving/<int:pk>/', views.post_archiving, name='post_archiving'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('feed/', views.FollowingPostListView.as_view(), name='feed'),
    path('like/<int:post_pk>/', views.like_post, name='like_post'),
    path('<int:post_id>/add-comment/', views.PostCommentCreateView.as_view(), name='add_comment'),
    path('delete-post-comment/<int:pk>/', views.delete_post_comment, name='delete_post_comment'),
    
]
