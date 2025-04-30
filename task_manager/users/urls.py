from django.urls import path

from task_manager.users import views

urlpatterns = [
    path("", views.UserIndex.as_view(), name="users_index"),
    path("create/", views.UserCreateView.as_view(), name="users_create"),
    path("<int:id>/delete/", views.UserDeleteView.as_view(),
        name="users_delete"),
    path("<int:id>/update/", views.UserUpdateView.as_view(),
        name="users_update"),
]
