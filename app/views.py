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
        
        
 
class doctor_patients(APIView):
    def get_object(self,id):
        try:
            return Patients.objects.get(id=id)
        except doctor.DoesNotExist:
            raise Http404
    def get(self,request,id):
        patients=[]
        reports=report_appiontment.objects.all().filter(doc=id) 
        for rep in reports:
            patients.append(rep.patient)
        serializer=PatinetSerializer(patients,many=True)
        return Response(serializer.data)

class doctor_reports(APIView):
    def get_object(self,id):
        try:
            return Patients.objects.get(id=id)
        except doctor.DoesNotExist:
            raise Http404
    def get(self,request,id):
        reports=report_appiontment.objects.all().filter(doc=id)
        from_date=self.request.query_params.get('from_date',None)
        to_date=self.request.query_params.get('to_date',None)
        year=datetime.now().year
        month=datetime.now().month
        day=datetime.now().day
        now=(str(year)+'-'+str(month)+'-'+str(day))
        date_format='%Y-%m-%d'

        
        if from_date :  
            if to_date:
                from_date=datetime.strptime(from_date,date_format)
                to_date=datetime.strptime(to_date,date_format)
                # to_date=to_date+timedelta(days=1)
                print(to_date)
                print('toooo')
                print(from_date)
                print('from_date')
                reports=reports.filter(date__range=[from_date,to_date])
            else:
                print(from_date)
                print('from_date')
                print('now')
                print(now)
                from_date=datetime.strptime(from_date,date_format)
                reports=reports.filter(date__range=[from_date,now])
        
        
        
        serializer=ReportSerializer(reports,many=True)
        return Response(serializer.data)
       
    
#reposrt_appointment

@api_view(['POST','GET'])
# def Reports(request):
#     reports=report_appiontment.objects.all()
#     if request.method == 'GET':
#         serializer=ReportSerializer(reports,many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer=ReportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
# @api_view(['GET','PUT','DELETE'])
# def Reports_id(request,id):
#     try:
#         reports=report_appiontment.objects.get(id=id)
#     except report_appiontment.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer=ReportSerializer(reports)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer=ReportSerializer(reports,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors)
#     elif request.method == 'DELETE':
#         reports.delete()
#         return Response(status=status.HTTP_201_CREATED)


class reports(generics.ListCreateAPIView):
    queryset=report_appiontment.objects.all()
    serializer_class=ReportSerializer
    
class reports_id(generics.RetrieveUpdateDestroyAPIView):
    queryset=report_appiontment.objects.all()
    serializer_class=ReportSerializer

 class filter_rep(APIView):
    def get(self,request,*args,**kwargs):
        queryset=report_appiontment.objects.all()
        flag=self.request.query_params.get('done',None)
        from_date=self.request.query_params.get('from_date',None)
        to_date=self.request.query_params.get('to_date',None)
        year=datetime.now().year
        month=datetime.now().month
        day=datetime.now().day
        now=(str(year)+'-'+str(month)+'-'+str(day))
        if from_date :  
            date_format='%Y-%m-%d'
            from_date=datetime.strptime(from_date,date_format)
            if to_date:
                to_date=datetime.strptime(to_date,date_format)
                # to_date=to_date+timedelta(days=1)
                print(to_date)
                print('toooo')
                queryset=queryset.filter(date__range=[from_date,to_date])
            else:
                print(from_date)
                print('from_date')
                print('now')
                print(now)
                now=datetime.strptime(now,date_format)
                queryset=queryset.filter(date__range=[from_date,now])

        
        serializer=ReportSerializer(queryset,many=True)
        return Response(serializer.data)
        
   
    
    
 
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
        
        
