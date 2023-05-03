from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','is_doctor','is_patient','is_secretary','password']

class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
    
class PatientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
class DoctorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
class SecretarytUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

class patient_serializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"},write_only=True) 
    password2=serializers.CharField(style={"input_type":"password"},write_only=True) 
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs={
            "password":{'write_only':True}
            
            
        }
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'] ,
            email=self.validated_data['email'] 
            
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':"password don't match"})
        user.set_password(password)
        user.is_patient=True
        user.save()
        patient.objects.create(user=user)
        
        
        return user
class doctor_serializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"},write_only=True) 
    password2=serializers.CharField(style={"input_type":"password"},write_only=True) 
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs={
            "password":{'write_only':True}
            
            
        }
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'] ,
            email=self.validated_data['email'] 
            
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':"password don't match"})
        user.set_password(password)
        user.is_doctor=True
        user.save()
        doctor.objects.create(user=user)
        
        
        return user
class secretary_serializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"},write_only=True) 
    password2=serializers.CharField(style={"input_type":"password"},write_only=True) 
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs={
            "password":{'write_only':True}
            
            
        }
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'] ,
            email=self.validated_data['email'] 
            
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':"password don't match"})
        user.set_password(password)
        user.is_secretary=True
        user.save()
        secretary.objects.create(user=user)
        
        
        return user

        
class patients(serializers.ModelSerializer):
    class Meta:
        model=patient
        fields=['patient_id','name',
                'gender',
                'image',
                'address',
                'phone_number',
                'age',
                'blood_type',
                'diabetes',
                'diabetes_type',
                'blood_preasure',
                ]
class doctors(serializers.ModelSerializer):
    class Meta:
        model=doctor
        fields=[
            'name',
            'doc_id',
                'gender',
                'image',
                "address",
                "phone_number",
                "age",
                "qualifications",
                
            
            
            ]
class secretaries(serializers.ModelSerializer):
    class Meta:
        model=secretary
        fields=['name',
                'gender',
                'image',
                "address",
                "phone_number",
                "age",
            
            ]




class PatinetSerializer(serializers.ModelSerializer):
    class Meta:
        model=patient
        fields='__all__'
        # read_only_field=['id']
    # def createtoken()
        
            
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=report_appiontment
        fields='__all__'
class SecreatarySerializer(serializers.ModelSerializer):
    class Meta:
        model=secretary
        fields='__all__'
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=doctor
        # fields='__all__'
        fields=['id','name','gender','address','username','phone_number','password','age','qualifications','salary','patients']

