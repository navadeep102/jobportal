from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import RegisterSerializer

from .models import Job
from .serializers import JobSerializer

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"})

    return Response(serializer.errors)
#models job schema 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):

    serializer = JobSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(posted_by=request.user)

        return Response(serializer.data)

    return Response(serializer.errors)

#read api
@api_view(['GET'])
def read_jobs(request):

    jobs = Job.objects.all()

    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)

#update api
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request, pk):

    job = Job.objects.get(id=pk)

    serializer = JobSerializer(job, data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)

#delete api
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job(request, pk):

    job = Job.objects.get(id=pk)

    job.delete()

    return Response({
        "message": "Job deleted"
    })