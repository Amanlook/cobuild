from django.urls import include, path
from .views import *

urlpatterns = [
    path('create-user/', UserCreateAPI.as_view()),
    path('user-list/', UserListAPI.as_view()),
    path('user-detail/<pk>/', UserDetailedAPI.as_view()),
    path('otp-verification/', OTPVerify.as_view()),
    path('reset-password/', UserResetPassword.as_view()),
    path('role-list/', RoleList.as_view()),
]
