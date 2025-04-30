from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path("", views.TaskIndex.as_view(), name="tasks_index"),
    path("<int:id>/", views.TaskShowView.as_view(), name="tasks_show"),
    path("create/", views.TaskCreateView.as_view(), name="tasks_create"),
    path("<int:id>/delete/", views.TaskDeleteView.as_view(),
        name="tasks_delete"),
    path("<int:id>/update/", views.TaskUpdateView.as_view(),
        name="tasks_update"),
]
