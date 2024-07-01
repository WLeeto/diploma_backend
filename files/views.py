import datetime

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from files.models import UserFile
from files.serializers import UserFilesSerializer, FileUploadSerializer, AdminUserFullStatSerializer, \
    FileUpdateSerializer

User = get_user_model()


class UserFiles(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserFilesSerializer(UserFile.objects.filter(user=request.user), many=True)
        return Response(serializer.data)


class Files(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, file_id):
        try:
            file = UserFile.objects.get(pk=file_id)
            if file.user != request.user and not request.user.is_staff:
                return Response(status=status.HTTP_403_FORBIDDEN)
            file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            print(ex)  # TODO Не поленись подключить логер
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # TODO Проверка на размер
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            user_file = serializer.save(user=request.user)
            return Response({
                'id': user_file.id,
                'filename': user_file.filename,
                'extension': user_file.extension,
                'file': user_file.file.url,
                'size': user_file.size,
                'uploaded_date': user_file.uploaded_date
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, file_id):
        try:
            file = UserFile.objects.get(id=file_id)
            file.last_download_date = datetime.datetime.now()
            file.save()

            return FileResponse(open(file.file.path, 'rb'))
        except Exception as ex:
            print(ex)  # TODO Не поленись подключить логер
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, file_id):
        try:
            file = UserFile.objects.get(pk=file_id)
            if file.user != request.user and not request.user.is_staff:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = FileUpdateSerializer(file, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print(ex)  # TODO: Не поленись подключить логер
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Admin(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = AdminUserFullStatSerializer(users, many=True)
        return Response(serializer.data)


class AddComment(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, file_id):
        try:
            comment = request.data.get('commentary')
            file = UserFile.objects.get(pk=file_id)
            if file.user != request.user and not request.user.is_staff:
                return Response(status=status.HTTP_403_FORBIDDEN)
            file.commentary = comment
            file.save()
            serializer = UserFilesSerializer(file)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)  # TODO Не поленись подключить логер
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ShareLinks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            file = UserFile.objects.get(pk=file_id)
            if file.user != request.user and not request.user.is_staff:
                return Response(status=status.HTTP_403_FORBIDDEN)

            current_site = get_current_site(request)
            if request.is_secure():
                base_url = f'https://{current_site.domain}'
            else:
                base_url = f'http://{current_site.domain}'

            share_link = f'{base_url}/files/getbylink/?share_link={file.link_hash}'
            return Response({'status': 'ok', 'share_link': share_link}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)  # TODO Не поленись подключить логер
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetByLink(APIView):
    # TODO Можно убрать аутентификацию и добавить тротлинг
    permission_classes = [AllowAny]

    def get(self, request):
        share_link = request.query_params.get('share_link')
        try:
            file = UserFile.objects.get(link_hash=share_link)
            file.last_download_date = datetime.datetime.now()
            file.save()
            return FileResponse(open(file.file.path, 'rb'))
        except UserFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print(ex)  # TODO Не поленись подключить логер
            return Response(status=status.HTTP_400_BAD_REQUEST)



