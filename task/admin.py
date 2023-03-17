from django.contrib import admin
from task.models import Task,TaskRating


@admin.register(Task)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'modified_at',)
    search_fields = ('title',)
    list_per_page = 5

admin.site.register([TaskRating])
