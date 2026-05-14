from rest_framework import serializers
from .models import ApplyJob, Job, SaveJob, User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = [
    'id',
    'title',
    'company',
    'location',
    'salary',
    'description'
]

class ApplyJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyJob
        fields = '__all__'

class SaveJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaveJob
        fields = '__all__'