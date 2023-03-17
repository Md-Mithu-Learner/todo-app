from django.urls import path,include
from rest_framework.routers import DefaultRouter
from task.views.api_view import TaskApiView
from task.views.function_base_views import function_base_task_list_api_view,func_base_post_create_api_view,\
    func_base_post_detail_api_view,func_base_post_update_api_view,func_base_task_delete_api_view,func_base_tasks_api_view,\
    func_base_tasks_api_view_serializers,func_task_serial_api_view

from task.views.generic_views import TaskListApiView,TaskRetrieveApiView,TaskCreateApiView,TaskUpdateApiView,TaskDestroyApiView,\
    TaskListCreateApiView,TaskRetrieveUpdateDestroyAPIView

from task.views.task_viewset import TaskViewSet
app_name='task'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet,basename="tasks")

urlpatterns = [
    path('', include(router.urls)),
    path('func-task-list/',function_base_task_list_api_view,name='function_task_list' ),
    path('func-task-create/', func_base_post_create_api_view, name='function_task_create'),
    path('func-task-detail/<int:task_id>/', func_base_post_detail_api_view, name='function_task_detail'),
    path('func-task-update/<int:task_id>/', func_base_post_update_api_view, name='function_task_update'),
    path('func-task-delete/<int:task_id>/', func_base_task_delete_api_view, name='function_task_update'),
]

urlpatterns += [
    path('func-tasks/',func_base_tasks_api_view,name='func_task'),
]
urlpatterns += [
    path('func-tasks-serializers/',func_base_tasks_api_view_serializers,name='func_task_serilizers'),
    path('func-tasks-serial/<int:task_id>/',func_task_serial_api_view,name='func_task_serial_api_view'),

]
urlpatterns += [
    path('generic-task-list/',TaskListApiView.as_view(),name='generic_task_list'),
    path('generic-task-detail/<int:pk>/', TaskRetrieveApiView.as_view(), name='generic_task_detail'),
    path('generic-task-create/', TaskCreateApiView.as_view(), name='generic_task_create'),
    path('generic-task-update/<int:pk>/', TaskUpdateApiView.as_view(), name='generic_task_update'),
    path('generic-task-delete/<int:pk>/', TaskDestroyApiView.as_view(), name='generic_task_delete'),
    path('generic-tasks/', TaskListCreateApiView.as_view(), name='generic_tasks'),
    path('generic-tasks-TaskRetrieveUpdateDestroyAPIView/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(),name='generic_task')

]

urlpatterns += [
    path('task-api-view/', TaskApiView.as_view(), name='task_api_view'),
]