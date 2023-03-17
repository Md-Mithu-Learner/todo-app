import copy
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from task.models import Task
from task.serializers import TaskSerializers
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

@api_view(['get'])

def function_base_task_list_api_view(request,*args,**kwargs):
    try:
        task_queryset = Task.objects.all()

        if request.GET.get('status',None):
            task_queryset = task_queryset.filter(status=request.GET.get('status',None))
        response = []
        for task in task_queryset:
            task_obj = {
                'id' : task.id,
                'title' : task.title,
                'description' : task.description,
                'created_at' : task.created_at,
                'modified_at' : task.modified_at,
                'status': task.status,
                'assignee': task.assignee.id

            }
            response.append(task_obj)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
    return Response({'message' : 'SERVER ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def func_base_post_create_api_view(request,*args,**kwargs):
    try:
        given_title = request.data.get('title', None)
        given_description = request.data.get('description', None)
        given_assignee = request.data.get('assignee', None)
        Task.objects.create(title=given_title, description=given_description, assignee_id=given_assignee)
        return Response({"message": "created"}, status=status.HTTP_201_CREATED)
    except Exception as ex:
        print(ex)
    return Response({'message' : 'SERVER ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['get'])
def func_base_post_detail_api_view(request,task_id,*args,**kwargs):
    try:
        task_obj = Task.objects.get(id=task_id)
        task_obj = {
            'id': task_obj.id,
            'title': task_obj.title,
            'description': task_obj.description,
            'created_at': task_obj.created_at,
            'modified_at': task_obj.modified_at,
            'status': task_obj.status,
            'assignee': task_obj.assignee.id

        }
        return Response(task_obj,status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
    return Response({'message':'server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT','PATCH'])
def func_base_post_update_api_view(request,task_id,*args,**kwargs):
    try:
        task_obj = Task.objects.get(id=task_id)
        if request.data.get('title', None):
            task_obj.title = request.data['title']
        if request.data.get('description',None):
            task_obj.description = request.data['description']
        if request.data.get('assignee'):
            task_obj.assignee_id = request.data['assignee']
        task_obj.save()

        return Response({"message": "successful"}, status=status.HTTP_201_CREATED)
    except Exception as ex:
        print(ex)
    return Response({'message': 'SERVER ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def func_base_task_delete_api_view(request,task_id,*args,**kwargs):
    try:
        Task.objects.filter(id=task_id).update(status='deleted')

        return Response({'message': 'deleted'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        print(ex)
    return Response({'message': 'server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET','POST'])
def func_base_tasks_api_view(request,*args,**kwargs):
    try:
        if request.method == 'GET':
            task_queryset = Task.objects.all()

            if request.GET.get('status', None):
                task_queryset = task_queryset.filter(status=request.GET.get('status', None))
            response = []
            for task in task_queryset:
                task_obj = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'created_at': task.created_at,
                    'modified_at': task.modified_at,
                    'status': task.status,
                    'assignee': task.assignee.id

                }
                response.append(task_obj)
            return Response(response, status=status.HTTP_200_OK)
        else:
            given_title = request.data.get('title', None)
            given_description = request.data.get('description', None)
            given_assignee = request.data.get('assignee', None)
            Task.objects.create(title=given_title, description=given_description, assignee_id=given_assignee)
            return Response({"message": "created"}, status=status.HTTP_201_CREATED)
    except Exception as ex:
        print(ex)
    return Response({'message': 'server error!'},status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET','POST'])
def func_base_tasks_api_view_serializers(request,*args,**kwargs):
    try:
        if request.method == 'GET':
            task_queryset = Task.objects.all()

            if request.GET.get('status', None):
                task_queryset = task_queryset.filter(status=request.GET.get('status', None))
            response = TaskSerializers(instance=task_queryset,many=True)

            return Response(response.data, status=status.HTTP_200_OK)
        else:
            serializer = TaskSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        print(ex)
    return Response({'message': 'server error!'},status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET','PUT','PATCH'])
def func_task_serial_api_view(request,task_id,*args,**kwargs):
    try:
        task_obj=Task.objects.filter(id=task_id).first()
        if request.method == 'GET':
            response = TaskSerializers(instance=task_obj)
            return Response(response.data, status=status.HTTP_200_OK)
        else:
            copy_request = copy.deepcopy(request.data)
            if request.data.get('assignee',None):
                copy_request['assignee'] = User.objects.filter(id=request.data['assignee']).first()
            serializer = TaskSerializers(instance=task_obj,data=request.data)
            if serializer.is_valid():
                serializer.update(instance=task_obj,validated_data=copy_request)
                return Response(serializer.data,status.HTTP_200_OK)
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


    except Exception as ex:
        print(ex)
    return Response({'messge': "server error"},status.HTTP_500_INTERNAL_SERVER_ERROR)