from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.PostCreateAPIView.as_view(), name="create-post"),
    path('home/', views.HomeAPIView.as_view(), name= 'home'),
    path('post-detail/<int:pk>/', views.PostUpdateDeleteAPIView.as_view(), name='post-detail')
]
