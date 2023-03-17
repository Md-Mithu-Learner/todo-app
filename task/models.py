from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class TaskRating(models.Model):
    NAME_OPT = (
        ('excellent','Excellent'),
        ('good','Good'),
        ('poor','poor')
    )
    name = models.CharField(max_length=20,choices=NAME_OPT,default='good')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_OPT=(
        ('to-do','To DO'),
        ('in-progress','In Progress'),
        ('done','Done'),
        ('deleted','Deleted')
    )
    title=models.CharField(max_length=500)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=200,choices=STATUS_OPT,default='to-do')
    assignee =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    rating = models.ManyToManyField(TaskRating, blank=True, related_name='task_rating')

    def __str__(self):
        return self.title[:40]