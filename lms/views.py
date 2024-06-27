    
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
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  SectionDetailed(RetrieveAPIView):
    serializer_class = SectionSerializer
    def get_object(self, pk):
        try:
            return  Section.objects.get(pk=pk,is_deleted=False)
        except  Section.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
        "section" : ["exact"],
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
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubSectionDetailed(RetrieveAPIView):
    
    serializer_class = SubSectionSerializer
    def get_object(self, pk):
        try:
            return  SubSection.objects.get(pk=pk,is_deleted=False)
        except  SubSection.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
        "question_type" : ["exact"],
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
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionBankDetailed(RetrieveAPIView):
    serializer_class = QuestionBankSerializer
    def get_object(self, pk):
        try:
            return  QuestionBank.objects.get(pk=pk,is_deleted=False)
        except  QuestionBank.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst= self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "option" : ["exact"],
        "question" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active":["exact"]
       
    }
    serializer_class =  OptionSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        queryset =  Option.objects.filter(is_deleted=False).order_by('-id')
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
    
class OptionDetailed(RetrieveAPIView):
    serializer_class = OptionSerializer
    def get_object(self, pk):
        try:
            return  Option.objects.get(pk=pk,is_deleted=False)
        except  Option.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst= self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
        "duration": ["exact","lte","gte"],
        "max_marks" : ["exact","gte","lte"],
        "passing_marks" : ["exact","gte","lte"],
        "number_of_questions":["exact","gte","lte"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
        "is_active" : ["exact"],
        "is_free":["exact"],
        "price" : ["exact","gte","lte"],
        
    }
    # search_fields = ['name', 'description']
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
            return  Quiz.objects.get(pk=pk,is_deleted=False)
        except  Quiz.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
        "section" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
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
            return  QuizSection.objects.get(pk=pk,is_deleted=False)
        except  QuizSection.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
        "question" : ["exact"],
        "created_at" : ["exact", "date__gte", "date__lte"],
        "updated_at" : ["exact", "date__gte", "date__lte"],
     
    }
    serializer_class =SectionQuestionSerializer
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
        serializer = self.get_serializer(queryset,many=True)
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
            return  SectionQuestion.objects.get(pk=pk,is_deleted=False)
        except  SectionQuestion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
        "quiz" : ["exact"],
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
            return  QuizEnrollment.objects.get(pk=pk,is_deleted=False)
        except  QuizEnrollment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
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
        "quiz":["exact"],
        "question":["exact"],
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
            return  UserQuizQuestion.objects.get(pk=pk,is_deleted=False)
        except  UserQuizQuestion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    
    
    

class CourseCategoryList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = CourseCategorySerliazer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    
    def get_queryset(self):
        queryset = CourseCategory.objects.filter().order_by('-id')
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
    
class CourseCategoryDetailed(RetrieveAPIView):
    serializer_class = CourseCategorySerliazer
    def get_object(self, pk):
        try:
            return  CourseCategory.objects.get(pk=pk)
        except  CourseCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    


class CourseList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = CourseSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_deleted=False).order_by('-id')
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
    

class CourseDetailed(RetrieveAPIView):
    serializer_class = CourseSerializer
    def get_object(self, pk):
        try:
            return  Course.objects.get(pk=pk,is_deleted=False)
        except  Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    
    
class CourseSectionList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = CourseSectionSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset = CourseSection.objects.filter(is_deleted=False).order_by('-id')
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


class CourseSectionDetailed(RetrieveAPIView):
    serializer_class = CourseSectionSerializer
    def get_object(self, pk):
        try:
            return  CourseSection.objects.get(pk=pk,is_deleted=False)
        except  CourseSection.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    
    
class CourseContentList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = CourseContentSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset = CourseContent.objects.filter(is_deleted=False).order_by('-id')
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


class CourseContentDetailed(RetrieveAPIView):
    serializer_class = CourseContentSerializer
    def get_object(self, pk):
        try:
            return  CourseContent.objects.get(pk=pk,is_deleted=False)
        except  CourseContent.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)

class CourseContentFileList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = CourseContentFileSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset = CourseContentFile.objects.filter().order_by('-id')
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
    
    

class CourseContentFileDetailed(RetrieveAPIView):
    serializer_class = CourseContentFileSerializer
    def get_object(self, pk):
        try:
            return  CourseContentFile.objects.get(pk=pk,is_deleted=False)
        except  CourseContentFile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    
    
class CourseEnrollmentList(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = CourseEnrollmentSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    
    def get_queryset(self):
        queryset = CourseEnrollment.objects.filter(is_deleted=False).order_by('-id')
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
    
    
class CourseEnrollmentDetailed(RetrieveAPIView):
    serializer_class = CourseEnrollmentSerializer
    def get_object(self, pk):
        try:
            return  CourseEnrollment.objects.get(pk=pk,is_deleted=False)
        except  CourseEnrollment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
       
        inst = self.get_object(pk)
        serializer =  self.get_serializer(inst)
        return Response(serializer.data)
    

    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = self.get_serializer(
            inst, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.is_deleted=True
        inst.save()
        return Response(status=status.HTTP_200_OK)
    
    
    

    
    
    

    