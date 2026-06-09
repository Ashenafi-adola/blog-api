from django.urls import path
from . import views

urlpatterns = [
    path('create-account/', views.CreateAccountAPIView.as_view(), name='create-account'),
    path('get-user-id/<str:username>/', views.GetUserIdAPIView.as_view(), name='get-user-id')
]
