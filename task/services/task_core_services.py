from django.db.models import Q
from task.models import Task
class TaskCoreServices:
    @staticmethod
    def get_filtered_task_queryset(task_queryset, filters=None, search_keyword=None):
        task_queryset = Task.objects.all()
        if search_keyword:
             task_queryset = task_queryset.filter(
                 Q(title__icontains = search_keyword)|
                 Q(description__icontains=search_keyword)
            )
        if not filters:
            return task_queryset
        if filters.get('status', None):
            task_queryset = task_queryset.filter(status=filters['status'])

        if filters.get('rating', None):
            task_queryset = task_queryset.filter(rating__name=filters['rating'])
        return task_queryset