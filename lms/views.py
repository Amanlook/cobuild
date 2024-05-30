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
            serializer.save(status=True, created_by=self.request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  SchoolDetailed(RetrieveAPIView):
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