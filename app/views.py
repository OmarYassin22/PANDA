from django.shortcuts import render,get_object_or_404
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serilaizers import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView

#patinets
@api_view(['POST','GET'])
def Patients(request):
    pat=patient.objects.all()
    if request.method == 'GET':
        serializer=PatinetSerializer(pat,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=PatinetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])           
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def Patients_id(request,id):
    try:
        pat=patient.objects.get(id=id)
    except patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer=PatinetSerializer(pat)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer=PatinetSerializer(pat,data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])           
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        pat.delete()
        return Response(status=status.HTTP_201_CREATED)

#doctors

class Doctors(APIView):
    def post(self,request):
        serializer=DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])           
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        doc=doctor.objects.all()
        serializer=DoctorSerializer(doc,many=True)
        return Response(serializer.data)

class Doctors_id(APIView):
    def get_object(self,id):
        try:
            return doctor.objects.get(id=id)
        except doctor.DoesNotExist:
            raise Http404

    def get(self,request,id):
        doc=self.get_object(id)
        serializer=DoctorSerializer(doc)
        return Response(serializer.data)
    def put(self,request,id):
        doc=self.get_object(id)
        serializer=DoctorSerializer(doc,data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])           
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        doc=self.get_object(id)
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
#reposrt_appointment

@api_view(['POST','GET'])
def Reports(request):
    reports=report_appiontment.objects.all()
    if request.method == 'GET':
        serializer=ReportSerializer(reports,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def Reports_id(request,id):
    try:
        reports=report_appiontment.objects.get(id=id)
    except report_appiontment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer=ReportSerializer(reports)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer=ReportSerializer(reports,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        reports.delete()
        return Response(status=status.HTTP_201_CREATED)


#secretary

class Secretary(APIView):
    def post(self,request):
        serializer=SecreatarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])           
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        sec=secretary.objects.all()
        serializer=SecreatarySerializer(sec,many=True)
        return Response(serializer.data)

class Secretary_id(APIView):
    def get_object(self,id):
        try:
            return secretary.objects.get(id=id)
        except secretary.DoesNotExist:
            raise Http404

    def get(self,request,id):
        sec=self.get_object(id)
        serializer=SecreatarySerializer(sec)
        return Response(serializer.data)
    def put(self,request,id):
        sec=self.get_object(id)
        serializer=SecreatarySerializer(sec,data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])           
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        sec=self.get_object(id)
        sec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        