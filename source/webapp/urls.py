from django.urls import path
from webapp.views.base import IndexView
from webapp.views.tasks import (
    AddView, DetailView, UpdateView,
    DeleteView, ConfirmDelete, TasksView
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tasks', TasksView.as_view(), name='tasks_view'),
    path('task/<int:pk>/', DetailView.as_view(), name='detail_view'),
    path('tasks/add', AddView.as_view(), name='add_view'),
    path('task/<int:pk>/update/', UpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', DeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/confirm_delete/', ConfirmDelete.as_view(), name='confirm_delete')
]
