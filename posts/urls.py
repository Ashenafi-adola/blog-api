from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.PostCreateAPIView.as_view(), name="create-post"),
    path('home/', views.HomeAPIView.as_view(), name= 'home'),
    path('post-detail/<int:pk>/', views.PostUpdateDeleteAPIView.as_view(), name='post-detail'),
    path('add-comment/<int:pk>/', views.AddCommentAPIView.as_view(), name="add-comment"),
    path('post-like/<int:pk>/', views.LikeAPIView.as_view(), name="like"),
    path('post-dislike/<int:pk>/', views.DisLikeAPIView.as_view(), name="dislike"),
    path('views/<int:pk>/', views.ViewsAPIView.as_view(), name='views')
]
