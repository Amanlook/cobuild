import datetime
from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions, status, filters
from cobuild.otp import OtpMixin
from cobuild.pagination import PaginationSize20
from users.models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from cobuild.settings import DEFAULT_PASS_WORD
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView

class UserCreateAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self,request):
        return Response({})
    
    def post(self, request, format=None):
        print("-----------------------------------------")
        password = request.data.get('password', None)
        if password is None:
            request.data._mutable = True
            request.data['password'] = str(DEFAULT_PASS_WORD)
            if "role" not in request.data:
                request.data['role'] = 12
        avtar = request.FILES.get('avtar', None)
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():   
            data = serializer.save(is_active=True, avtar = avtar)
            refresh = RefreshToken.for_user(data)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response = {
                "user_data" : serializer.data,
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPI(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['email', 'first_name', 'last_name','id', 'contact','dob','is_staff','is_active','date_joined','role','counter','last_attempt','last_activity','created_at','updated_at']
    serializer_class = UserSerializerDetailed
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        queryset = User.objects.filter(is_deleted=False).order_by('-date_joined')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_param = self.request.query_params.get("page")
        if page_param:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return Response(self.get_paginated_response(serializer.data))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class UserDetailedAPI(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk,is_deleted=False)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializerDetailed(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializerDetailed(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted = True
        inst.save()        
        return Response(status=status.HTTP_200_OK)
    
class OTPVerify(APIView, OtpMixin):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        contact = self.request.query_params.get('contact')
        if not contact:
            return Response({"message": "email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_inst = User.objects.get(contact=contact)
        except User.DoesNotExist:
            return Response({"message": "User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        if user_inst.counter > 3 and user_inst.updated_at.replace(tzinfo=None) + datetime.timedelta(seconds=120) < datetime.datetime.now().replace(tzinfo=None):
            user_inst.counter = 1
        user_inst.counter += 1
        user_inst.save()
        if user_inst.counter < 18:
            otp = self.generate_otp(contact, user_inst.counter)
            return Response({'status': 200, 'message': "OTP sent successfully", "otp" : str(otp)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You have tried the maximum number of times. Please try again after 2 minutes."}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        data = request.data
        contact = data.get('contact')
        otp = data.get('otp')
        if not (otp and contact):
            return Response({
                'error': True,
                'message': 'Password, OTP and Email is required.'
            })
        try:
            user = User.objects.get(contact=contact)
        except User.DoesNotExist:
            return Response({"message": "User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        if otp and self.verify_otp(contact,user.counter,otp):
            return Response({
                'success': True,
                'message': 'OTP Verified!'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Invalid OTP.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
class UserResetPassword(APIView):
    permission_classes = [permissions.AllowAny]
    def put(self, request, *args, **kwargs):
        data = request.data
        contact = data.get('contact')
        password = data.get('password')
        try:
            user = User.objects.get(contact=contact)
        except User.DoesNotExist:
            return Response({"message": "User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.is_active = True
        user.save()
        return Response({
            'message': 'Password has been reset successfully!'
        }, status=status.HTTP_200_OK)
        
class RoleList(ListAPIView):
    
    def get(self, request, *args, **kwargs):
        data = Role.objects.all().order_by("id").values()
        return Response(data, status=status.HTTP_200_OK)
