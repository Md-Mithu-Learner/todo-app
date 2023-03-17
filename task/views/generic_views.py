from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from task.models import Task
from task.permissions import HasObjAccess
from task.serializers import TaskSerializers, TaskListCreateSerializer

class TaskListApiView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListCreateSerializer

class TaskRetrieveApiView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

class TaskCreateApiView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

class TaskUpdateApiView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

class TaskDestroyApiView(DestroyAPIView):
    queryset = Task.objects.all()


class TaskListCreateApiView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListCreateSerializer

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (HasObjAccess,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

