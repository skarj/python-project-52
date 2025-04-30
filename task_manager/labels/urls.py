from django.urls import path

from task_manager.labels import views

urlpatterns = [
    path("", views.LabelIndex.as_view(), name="labels_index"),
    path("create/", views.LabelCreateView.as_view(), name="labels_create"),
    path("<int:id>/delete/", views.LabelDeleteView.as_view(),
        name="labels_delete"),
    path("<int:id>/update/", views.LabelUpdateView.as_view(),
        name="labels_update"),
]
