from django.urls import path

from api.views import api_overview, task_list, task_detail, task_create, task_delete, task_update, TaskListCreate, \
    TaskRetrieveUpdateDestroy

urlpatterns = [
    path('', api_overview),
    path('task-list/', task_list),
    path('task-create/', task_create),
    path('task-delete/<str:pk>/', task_delete),
    path('task-update/<str:pk>/', task_update),
    path('task-detail/<str:pk>/', task_detail),
    path('task-list2/', TaskListCreate.as_view()),
    path('task-detail2/<str:pk>/', TaskRetrieveUpdateDestroy.as_view()),
]
