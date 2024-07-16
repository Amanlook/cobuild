    
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


