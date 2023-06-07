from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from rest_framework import generics, status,filters
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from .serilaizers import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework import generics,viewsets
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import *
from .serilaizers import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import Http404

#patinets
@api_view(['POST','GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def Patients(request):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = (IsAuthenticated)

   
    if request.method == 'GET':
        pat=patient.objects.all()
        serializer=PatinetSerializer(pat,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=PatinetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])           
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      

class patient_view(APIView):
    def get(self,request):
        profiles=profile.objects.get(user=request.user)
        serializer=patient_profile_serializer(profiles)
        return Response(serializer.data)
    def post(self,request):
        pass



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

class doctor_list(generics.ListAPIView):
    serializer_class=doctors
    queryset=doctor.objects.all()

        
class Doctors_id(generics.GenericAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class=doctors
    def get(self,request):
        try:
            user=User.objects.get(username=request.user.username)
            doc=doctor.objects.get(user=user)
            serializer=doctors(doc)
            return Response(serializer.data)
        except:
            message="unauthorized access, you are't a doctor"
            return Response(message)
    def put(self,request,id):
        if request.user.is_doctor:
            user=User.objects.get(username=request.user.username)
            doc=doctor.objects.get(user=user)
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            else:return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            message="unauthorized access, you are't a doctor"
            return Response(message)
    def delete(self,request,id):
        doc=self.get_object(id)
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
  

class doctor_patients(APIView):
 
    def get(self,request):
        patients=[]
        user=User.objects.get(username=request.user.username)
        doc=doctor.objects.get(user=user)
        reports=report_appiontment.objects.all().filter(doc=doc) 
        for rep in reports:
            patients.append(rep.patient)
        serializer=PatinetSerializer(patients,many=True)
        return Response(serializer.data)

class doctors_patiets_valid(APIView):
    pass
# # class doctor_reports(APIView):
#     # def get_object(self,id):
#     #     try:
#     #         return Patients.objects.get(id=id)
#     #     except doctor.DoesNotExist:
#     #         raise Http404
#     def get(self,request):
#         try:
#             user=User.objects.get(username=request.user.username)
#             doc=doctor.objects.get(user=user)
#             print(request.user.username)
#             reports=report_appiontment.objects.all().filter(doc=doc)
#             from_date=self.request.query_params.get('from_date',None)
#             to_date=self.request.query_params.get('to_date',None)
#             year=datetime.now().year
#             month=datetime.now().month
#             day=datetime.now().day
#             now=(str(year)+'-'+str(month)+'-'+str(day))
#             date_format='%Y-%m-%d'

            
#             if from_date :  
#                 if to_date:
#                     from_date=datetime.strptime(from_date,date_format)
#                     to_date=datetime.strptime(to_date,date_format)
#                     # to_date=to_date+timedelta(days=1)
#                     print(to_date)
#                     print('toooo')
#                     print(from_date)
#                     print('from_date')
#                     reports=reports.filter(date__range=[from_date,to_date])
#                 else:
#                     print(from_date)
#                     print('from_date')
#                     print('now')
#                     print(now)
#                     from_date=datetime.strptime(from_date,date_format)
#                     reports=reports.filter(date__range=[from_date,now])
            
            
            
#             serializer=ReportSerializer(reports,many=True)
#             return Response(serializer.data)
#         except:
#             message='unauthorized access'
#             return Response(message)
class doctor_reports(generics.GenericAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset=report_appiontment.objects.all()
    serializer_class=ReportSerializer
    def get(self,request):
        try:
            user=User.objects.get(username=request.user.username)
            doc=doctor.objects.get(user=user)
            rep=report_appiontment.objects.get(doc=doc)
            serializer=self.get_serializer(rep)
            
            return Response(serializer.data)
        except:
            message="there is no reports"
            return Response(message)
            
    def put(self,request):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except:
            pass

#reposrt_appointment

# @api_view(['POST','GET'])
# def Reports(request):
#     reports=report_appiontment.objects.all()
#     done =report_appiontment.objects.filter(done=True)
#     if request.method == 'GET':
#         serializer=ReportSerializer(reports,many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer=ReportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class patient_reports(generics.GenericAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset=report_appiontment.objects.all()
    serializer_class=ReportSerializer
    def get(self,request):
        try:
            user=User.objects.get(username=request.user.username)
            pat=patient.objects.get(user=user)
            rep=report_appiontment.objects.get(patient=pat)
            serializer=self.get_serializer(rep)
            
            return Response(serializer.data)
        except:
            message="there is no reports"
            return Response(message)
            
    def put(self,request):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except:
            pass

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

# # class report_viewset(viewsets.ModelViewSet):
#     queryset=report_appiontment.objects.all()
#     serializer_class=ReportSerializer
    
    
    
    
#     filter_backends=[DjangoFilterBackend,filters.SearchFilter]
#     # search_fields=['id']
#     filter_fields=['id']

    

        
        serializer=ReportSerializer(queryset,many=True)
        return Response(serializer.data)
        

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
        


class signup_patients(APIView):
    # serializer_class=patient_serializer
    
    def post(self,request,*args, **kwargs):
        try:
            serializer=patient_serializer(data=request.data['user'])
            serializer.is_valid(raise_exception=True)
                
            user=serializer.save()
            if request.data['profile']:

                prof=request.data['profile']
                print(prof)
                profile=patient.objects.filter(user=User.objects.get(username=serializer.data['username'])).update(**prof)
                print(profile)
                prof_ser=patients(patient.objects.get(user=User.objects.get(username=serializer.data['username'])))
                return Response({
                    "user":serializer.data,
                    "profile":prof_ser.data,
                    "token":Token.objects.get(user=user).key,
                    "message":"account created successfully"
                })
            else:
                prof=None
                return Response({
                    "user":serializer.data,
                    "token":Token.objects.get(user=user).key,
                    "message":"account created successfully"
                })
        except:
            return Response({'message':'there is error in data'})
class signup_secretaries(generics.GenericAPIView):
    serializer_class=secretary_serializer
    
    def post(self,request,*args, **kwargs):
        try:
            serializer=secretary_serializer(data=request.data['user'])
            serializer.is_valid(raise_exception=True)
                
            user=serializer.save()
            if request.data['profile']:

                prof=request.data['profile']
                print(prof)
                profile=secretary.objects.filter(user=User.objects.get(username=serializer.data['username'])).update(**prof)
                print(profile)
                prof_ser=secretaries(secretary.objects.get(user=User.objects.get(username=serializer.data['username'])))
                return Response({
                    "user":serializer.data,
                    "profile":prof_ser.data,
                    "token":Token.objects.get(user=user).key,
                    "message":"account created successfully"
                })
            else:
                prof=None
                return Response({
                    "user":serializer.data,
                    "token":Token.objects.get(user=user).key,
                    "message":"account created successfully"
                })
        except:
            return Response({'message':'There is error in data'})
class signup_doctors(generics.GenericAPIView):
    serializer_class=doctor_serializer

    def post(self,request,*args, **kwargs):
        try:
            flag=User.objects.filter(username=request.data.get('user')).count()
            if flag == 0:
                serializer=doctor_serializer(data=request.data['user'])
                if serializer.is_valid(raise_exception=True):
                        
                    user=serializer.save()
                    if request.data.get('profile'):
                        prof=request.data['profile']
                        print(prof)
                        profile=doctor.objects.filter(user=User.objects.get(username=serializer.data['username'])).update(**prof)
                        print(doctor.objects.get(user=User.objects.get(username=serializer.data['username'])))
                        prof_ser=patients(doctor.objects.get(user=User.objects.get(username=serializer.data['username'])))
                        return Response({
                            "user":serializer.data,
                            "profile":prof_ser.data,
                            "token":Token.objects.get(user=user).key,
                            "message":"account created successfully"
                        })
                    elif request.data.get('qualifications'):
                        quals=request.data.get('qualifications')
                    else:
                        prof=None
                        return Response({
                            "user":serializer.data,
                            "token":Token.objects.get(user=user).key,
                            "message":"account created successfully"
                        })
                else:
                    message=[]
                    message.append(serializer.errors)
                    return Response({'errors':message},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'errors':"A user with that username already exists."},status=status.HTTP_400_BAD_REQUEST)
        except:
                return Response({'message':'there is error in data'})
class signup_doctors_info(generics.GenericAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class=doctors
    def get(self,request):
        if request.user.is_doctor:
            try:
                print(request.user.username)
                print('###########################')
                user=User.objects.get(username=request.user.username)
                doc=doctor.objects.get(user=user)
                user_serializer=doctor_serializer(user)
                doc_serializer=doctors(doc)
                respose={
                    "account info":user_serializer.data,
                    "personal info":doc_serializer.data,
                        }
                return Response(respose)
            except:
                message='AnonymousUser'
                return Response(message)
        message='Not a Doctor'
        return Response(message)
    def put(self,request):
        if request.user.is_doctor:
            try:
                serializer=self.get_serializer(data=request.data)
                print('####################################################')
                print(serializer.errors)
                serializer.is_valid(raise_exception=True)
                user=serializer.save()
                return Response(serializer.data)
            except:
                message='AnonymousUser'
                return Response(message)
        message='Not a Doctor'
        return Response(message)
class ListPatients(APIView):
    authentication_classes = [TokenAuthentication]
    
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset=patient.objects.all()
        serializer=patients(queryset,many=True)
        
        if request.user and request.user.is_doctor:
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            
            return Response({'message':'unauthorized access detected'},status=status.HTTP_401_UNAUTHORIZED)
            
class ListDoctors(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        queryset=doctor.objects.all()
        serializer=doctors(queryset,many=True)
        
        if request.user :
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            
            return Response({'message':'unauthorized access detected'},status=status.HTTP_401_UNAUTHORIZED)
            
class ListSecretaries(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        queryset=secretary.objects.all()
        serializer=secretaries(queryset,many=True)
        
        if request.user :
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            
            return Response({'message':'unauthorized access detected'},status=status.HTTP_401_UNAUTHORIZED)

class log_in(APIView):
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return Response({'message':'login successfully',
                            'token':Token.objects.get(user=user).key})
        return Response({'message':'please make sure from user name and password'})
class log_out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response({'message':'logged out successful'},status=status.HTTP_200_OK)
        
                   
class PatientProfile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        try:
            pat=patient.objects.get(user=request.user)
            user=User.objects.get(username=pat)
            user_serialzer=UserSerializer2(user)
            serializer=patients(pat)
                
            response={
                'account_info':user_serialzer.data,
                'medical_info':serializer.data,
            }
                
            return Response(response)
        except:
            message="there is no patinet"
            return Response(message)
            
        
    
   
class PatientProfileEdite(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    # serializer_class=patients
    def get(self,request):
        pat=patient.objects.get(user=request.user)
        user=User.objects.get(username=pat)
        user_serialzer=UserSerializer(user)
        serializer=patients(pat)
            
        print(user_serialzer.data)
        response={
            'account_info':user_serialzer.data,
            'medical_info':serializer.data,
        }
            
        return Response(response)
    def put(self,request):
        pat=patient.objects.get(user=request.user)
        user=User.objects.get(username=pat)
        message=[]
        if request.POST.get('username'):
            user.username=request.data['username']
        if request.POST.get('password'):
            user.password=make_password(request.data['password'])
        if request.POST.get('email'):
            user.email=request.data['email']
        user.save()
        user_serialzer=PatientUserSerializer(user)
        if request.POST.get('name'):
            pat.name=request.data['name']
        if request.POST.get('gender'):
            if request.data['gender']  in ['male','female']:
                pat.gender=request.data['gender']
            else:message.append('invalid gender input ')
        if request.POST.get('image'):
            pat.image=request.data['image']
        if request.POST.get('address'):
            pat.address=request.data['address']
        if request.POST.get('phone_number'):
            try:
                pat.phone_number=request.data['phone_number']
            except:
                message.append("please enter number for your phone")
        if request.POST.get('age'):
            pat.age=request.data['age']
        if request.POST.get('blood_type'):
            if request.data['blood_type'] in ['O+' 'O-','A+','A-', 'B+','B-', 'C+', 'C-','AB+', 'AB-']:
                pat.blood_type=request.data['blood_type']
            else: message.append("invalid blood type")
        if request.POST.get('diabetes'):
            pat.diabetes=request.data['diabetes']
        if request.POST.get('diabetes_type'):
            if request.data['diabetes_type']  =='type1' or request.data['diabetes_type']=='type2':
                pat.diabetes_type=request.data['diabetes_type']
            else:message.append('invalid diabetes_type input, chose from type1 or type2')
        if request.POST.get('blood_preasure'):
            if request.data['blood_preasure'] not in [True,False]:
                pat.blood_preasure=request.data['blood_preasure']
            else:message.append('invalid blood_preasure input')
        if request.POST.get('diseases'):
            pat.diseases=request.data['diseases']
        if request.POST.get('patient_id'):
            patient_ids=patient.objects.all()
            patient_ids=patient_ids.values('patient_id')
            print(patient_ids)
            if request.data['patient_id'] not in patient_ids:
                pat.patient_id=request.data['patient_id']
            else:message.append("patient id already exist, please chose another one")
            
            
        pat.save()
        serializer=patients(pat)
        response={
            'account_info':user_serialzer.data,
            'medical_info':serializer.data,
            'message':message
        }
            
        return Response(response)
    
