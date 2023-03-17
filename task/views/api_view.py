from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from task.models import Task
from rest_framework.permissions import IsAuthenticated
from task.services.task_core_services import TaskCoreServices


class TaskApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, *args, **kwargs):
        return Response({"message": "hello post"}, status=status.HTTP_200_OK)

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            filters = {
                'status': request.GET.get('status', None),
                'rating': request.GET.get('rating', None)
            }
            search_keyword = request.GET.get('search', None)
            task_qs = Task.objects.all()
            task_filtered_qs = TaskCoreServices().get_filtered_task_queryset(task_qs, filters, search_keyword)
            response = []
            for task in task_filtered_qs:
                response.append({
                    "id": task.id,
                    "title": task.title
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"MESSAGE": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
