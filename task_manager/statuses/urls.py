from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.StatusIndex.as_view(), name='statuses_index'),
    path('create/', views.StatusCreateView.as_view(), name='statuses_create'),
    path('<int:id>/delete/', views.StatusDeleteView.as_view(), name='statuses_delete'),
    path('<int:id>/update/', views.StatusUpdateView.as_view(), name='statuses_update'),
]
