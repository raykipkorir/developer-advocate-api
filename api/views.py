from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer
from .twitter_api import main

def routers(request):
    return render(request, "api/home.html")

class AdvocateListCreate(generics.ListCreateAPIView):
    serializer_class = AdvocateSerializer
    queryset = Advocate.objects.all()
    pagination_class = PageNumberPagination


class AdvocateDetail(generics.GenericAPIView):
    serializer_class = AdvocateSerializer
    queryset = Advocate.objects.all()

    def get(self, request, username):
        main(username)
        advocate = get_object_or_404(self.queryset, username=username)
        serializer = AdvocateSerializer(instance=advocate)
        return Response({"advocate":serializer.data}, status=status.HTTP_200_OK)



class CompanyList(generics.ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    pagination_class = PageNumberPagination


class CompanyDetail(generics.GenericAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get(self, request, username):
        company = get_object_or_404(self.queryset, username=username)
        serializer = CompanySerializer(instance=company)
        return Response({"company":serializer.data}, status=status.HTTP_200_OK)