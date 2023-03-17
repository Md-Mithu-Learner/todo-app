from rest_framework import serializers

from task.models import Task,TaskRating
from django.contrib.auth import get_user_model
User = get_user_model()

class UserNameEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')


class TaskRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRating
        fields = '__all__'

class TaskSerializers(serializers.ModelSerializer):
    class Meta:
            model = Task
            fields = '__all__'


class TaskListCreateSerializer(serializers.ModelSerializer):
    rating = TaskRatingSerializer(many=True,read_only=True)
    class Meta:
        model = Task
        fields = ('id','title','description','assignee','rating',)

    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['status'] = instance.status
        # user_obj = User.objects.get(id=instance.assignee_id)
        # data['assignee'] = {
        #     'id' : user_obj.id,
        #     'username' : user_obj.username,
        #     'email':user_obj.email,
        # }
        data['assignee'] = UserNameEmailSerializer(instance=instance.assignee).data
        return data

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title','status',)

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title','description','status',)