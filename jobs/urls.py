from django.urls import path
from .views import create_job, delete_job, read_jobs, register, update_job

urlpatterns = [
    path('register/', register),
    path('jobs/create/', create_job),
    path('jobs/', read_jobs),
    path ('jobs/update/<int:pk>/', update_job),
    path('jobs/delete/<int:pk>/', delete_job),
]