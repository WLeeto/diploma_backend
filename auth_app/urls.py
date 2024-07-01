from django.urls import path

from auth_app.views import RegisterUser, DeleteUser

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('deleteuser/<int:user_id>/', DeleteUser.as_view()),
]