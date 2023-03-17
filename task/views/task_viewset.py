from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from task.permissions import IsSuperUser
from task.serializers import TaskSerializers, TaskListSerializer, TaskDetailSerializer
from task.models import Task

from django.db.models import Q


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser)
    queryset = Task.objects.all()
    serializer_classes = {
        'list': TaskListSerializer,
        'retrieve': TaskDetailSerializer,
    }
    default_serializer_classes = TaskSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['status', 'description', 'rating__name']
    filterset_fields = ['status',]

    lookup_field = 'id'
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,self.default_serializer_classes['default'])

    def get_queryset(self):
        queryset = self.queryset.filter(~Q(status='deleted'))
        if self.request.GET.get('status', None):
            queryset = queryset.filter(status=self.request.GET['status'])
            queryset = self.filter_queryset(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "SERVER error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(ex)
        return Response({"message": "SERVER error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            print(ex)
        return Response({"message": "SERVER error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            if not self.queryset.filter(id=kwargs['id']).exists():
                return Response({'massage': 'content not found'},status=status.HTTP_204_NO_CONTENT)
            instance = self.get_object()
            serializer = self.get_serializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(ex)
        return Response({"message": "SERVER error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.status = 'deleted'
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            print(ex)
        return Response({"message": "SERVER error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False,methods=['GET'], url_path= 'get-task-list')
    def get_task_list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            response= []
            for task in queryset:
                response.append(task.id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "SERVER error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
