from django.urls import path

from files.views import UserFiles, Files, Admin, AddComment, ShareLinks, GetByLink

urlpatterns = [
    path('user/', UserFiles.as_view()),
    path('<int:file_id>/', Files.as_view()),
    path('', Files.as_view()),
    path('admin/', Admin.as_view()),
    path('comments/<int:file_id>/', AddComment.as_view()),
    path('share_link/<int:file_id>/', ShareLinks.as_view()),
    path('getbylink/', GetByLink.as_view()),
]