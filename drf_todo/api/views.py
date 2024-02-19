from django.http import JsonResponse
from rest_framework import status
# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Task
from api.serializers import TaskSerializer


# Create your views here.
@api_view(["GET"])
def api_overview(request):
    api_urls = {
        "list": "/task-list/",
        "create": "/task-create/",
        "update": "/task-update/pk/",
        "delete": "/task-delete/pk"
    }
    return JsonResponse(api_urls)


@api_view(["GET"])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def task_detail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def task_delete(request, pk):
    try:
        task = Task.objects.get(id=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def task_update(request, pk):
    try:
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class TaskListCreate(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Require authentication


class TaskRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
