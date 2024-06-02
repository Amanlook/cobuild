    
import json
from django.shortcuts import render
from .serializers import *
from .models import *
from .serializers import *
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.http import Http404
from rest_framework.response import Response
from cobuild.pagination import PaginationSize20
from django.db import transaction
from itertools import zip_longest, chain, groupby
from django.db.models import CharField, Value
import datetime

# Create your views here.
class SectionList(ListAPIView):    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "name" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class =  SectionSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20

    def get_queryset(self):
        queryset =  Section.objects.filter(is_deleted=False).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  SectionDetailed(RetrieveAPIView):
    serializer_class = SectionSerializer
    def get_object(self, pk):
        try:
            return  Section.objects.get(pk=pk)
        except  Section.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    
    

class SubSectionList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "name" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class =  SubSectionSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        queryset =  SubSection.objects.filter(is_deleted=False).order_by('-id')
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
    
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SubSectionDetailed(RetrieveAPIView):
    
    serializer_class = SubSectionSerializer
    def get_object(self, pk):
        try:
            return  SubSection.objects.get(pk=pk)
        except  SubSection.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    

class QuestionBankList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "question" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class =  QuestionBankSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset =  QuestionBank.objects.filter(is_deleted=False).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionBankDetailed(RetrieveAPIView):
    serializer_class = QuestionBankSerializer
    def get_object(self, pk):
        try:
            return  QuestionBank.objects.get(pk=pk)
        except  QuestionBank.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
      
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    

class OptionList(ListAPIView):
    serializer_class =  OptionSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        question=self.request.query_params.get('question', None)
        queryset =  Option.objects.filter(is_deleted=False,question=question).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class OptionDetailed(RetrieveAPIView):
    serializer_class = OptionSerializer
    def get_object(self, pk):
        try:
            return  Option.objects.get(pk=pk)
        except  Option.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    

class QuizList(ListAPIView):
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "name" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class =  QuizSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset =  Quiz.objects.filter(is_deleted=False).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class QuizDetailed(RetrieveAPIView):
    serializer_class = QuizSerializer
    def get_object(self, pk):
        try:
            return  Quiz.objects.get(pk=pk)
        except  Quiz.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)


class QuizSectionList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "quiz" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class =  QuizSectionSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset =  QuizSection.objects.filter(is_deleted=False).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class QuizSectionDetailed(RetrieveAPIView):
    serializer_class = QuizSectionSerializer
    def get_object(self, pk):
        try:
            return  QuizSection.objects.get(pk=pk)
        except  QuizSection.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    

class SectionQuestionList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "section" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class =SectionQuestion
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset =  SectionQuestion.objects.filter(is_deleted=False).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SectionQuestionDetailed(RetrieveAPIView):
    serializer_class = SectionQuestionSerializer
    def get_object(self, pk):
        try:
            return  SectionQuestion.objects.get(pk=pk)
        except  SectionQuestion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    
class QuizEnrollmentList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "user" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class =  QuizEnrollmentSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset =  QuizEnrollment.objects.filter(is_deleted=False).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class QuizEnrollmentDetailed(RetrieveAPIView):
    serializer_class = QuizEnrollmentSerializer
    def get_object(self, pk):
        try:
            return  QuizEnrollment.objects.get(pk=pk)
        except  QuizEnrollment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    

class UserQuizQuestionList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
         "user" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
    }
    serializer_class = UserQuizQuestionSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset =  UserQuizQuestion.objects.filter(is_deleted=False).order_by('-id')
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
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class UserQuizQuestionDetailed(RetrieveAPIView):
    serializer_class = UserQuizQuestionSerializer
    def get_object(self, pk):
        try:
            return  UserQuizQuestion.objects.get(pk=pk)
        except  UserQuizQuestion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        user = self.get_object(pk)
        serializer =  self.get_serializer(user)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.get_serializer(
            user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    

    
    
    

    