from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.index, name='users_index'),
    path('create/', views.UserCreateView.as_view()),
]
