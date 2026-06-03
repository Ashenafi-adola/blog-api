from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.PostCreateAPIView.as_view(), name="create-post")
]
