from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers
from files.models import UserFile


User = get_user_model()


class UserFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFile
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ['file']


class FileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ['filename', 'commentary']


class AdminUserFullStatSerializer(serializers.ModelSerializer):
    total_size = serializers.SerializerMethodField()
    files_count = serializers.SerializerMethodField()
    all_files = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('total_size', 'files_count', 'all_files', 'user_info')

    def get_user_info(self, obj):
        return {
            "username": obj.username,
            "id": obj.id,
            "email": obj.email,
            "is_admin": obj.is_staff,
        }

    def get_total_size(self, obj):
        return UserFile.objects.filter(user=obj).aggregate(total_size=Sum('size'))['total_size']

    def get_files_count(self, obj):
        return UserFile.objects.filter(user=obj).count()

    def get_all_files(self, obj):
        files_qs = UserFile.objects.filter(user=obj)
        files_serializer = UserFilesSerializer(files_qs, many=True)
        return files_serializer.data
