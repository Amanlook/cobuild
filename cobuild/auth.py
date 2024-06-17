from django.conf import settings
from rest_framework.request import Request
from cobuild.otp import OtpMixin
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from users.serializers import UserLoginGetSerializer, UserLoginSerializer


class UserLoginAPIView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password', None)
            contact = request.data.get('contact', None)
            try:
                user_object = User.objects.get(contact=contact, is_active = True)
            except User.DoesNotExist:
                return Response({"message" : "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            valid_pass = user_object.password
            is_valid = check_password(password, valid_pass)
            resp ={}
            if is_valid:
                refresh = RefreshToken.for_user(user_object)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                resp["refresh_token"] = refresh_token
                resp["access_token"] = access_token
                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CurrentUser(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            current_user = self.request.user
            serializer = UserLoginGetSerializer(current_user)
            return Response(serializer.data)
        except Exception as e:
             return Response({"success":False,"message":"invalid user"})
            
    
class OTPLoginView(TokenObtainPairView, OtpMixin):
    
    def get(self, request, *args, **kwargs):
        params = self.request.query_params
        contact = params.get('contact', None)
        try:
            user_object = User.objects.get(contact=contact, is_active=True)
            contact = user_object.contact
        except User.DoesNotExist:
            return Response({"message" : "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        otp = self.generate_totp(contact)
        return Response({"message": "OTP send Successfully", "otp" : str(otp)}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        otp = data.get('otp', None)
        contact = data.get('contact', None)
        try:
            user_object = User.objects.get(contact=contact, is_active = True)
            contact = user_object.contact
        except User.DoesNotExist:
            return Response({"message" : "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        if otp:
            if not self.verify_totp(contact, otp):
                return Response({"message":"OTP Invalid Please try again.", "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user_object)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            resp = {
                "tokens" : {
                    "refresh_token" : refresh_token,
                    "access_token" : access_token
                },
         
            }
        return Response(resp, status=status.HTTP_200_OK)
