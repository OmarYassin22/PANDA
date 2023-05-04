from django.db import models
from django.db.models.signals import post_save
from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class User(AbstractUser):
    is_patient=models.BooleanField(default=False)
    is_doctor=models.BooleanField(default=False)
    is_secretary=models.BooleanField(default=False)
      def __str__(self):
        if self.is_doctor: 
            return str(self.username+' / doctor')
        elif self.is_secretary:
            return str(self.username+' / secretary')
        elif self.is_patient:
            return str(self.username+' / Patient')

        else:
            return str(self.username+' / Admin')  
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance,created,*args, **kwargs):
    if created:
        Token.objects.create(user=instance)

class doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="doctor_user")
    doc_id=models.CharField( max_length=50,default="not de")
    # presonal info
    genders = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]


    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=genders, default='Male',null=True,blank=True)
    image=models.ImageField(upload_to='photos/doctors/%y%m%d',default=None,null=True,blank=True)
    address = models.CharField(max_length=50, null=True, blank=True,default="There is No Address for communication ")
    phone_number = models.IntegerField( null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)



    def __str__(self):
        if self.user.username:
            return self.user.username
        elif self.name:
            return self.name
        else:
            return 'doctor'
            
    
class patient(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="User_patient")
    
    doctor=models.ManyToManyField(doctor, related_name="doctor")
    patient_id=models.CharField(max_length=50,blank=True,null=True)
    genders=[
        ('Male','Male'),
        ('Female','Female')
    ]
    blood_types = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C-', 'C-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),

    ]
    diabetes_types=[
        ('type 1', 'type 1'),
        ('type 2', 'type 2')
    ]
    
    name = models.CharField(max_length=50,null=True)
    gender = models.CharField(max_length=50, choices=genders,default="Male",null=True,blank=True )
    image=models.ImageField(upload_to='patient/%y%m%d',default='None',null=True,blank=True)
    address = models.CharField(max_length=50, null=True, blank=True,default="There is no current address")
    phone_number = models.IntegerField( null=True, blank=True,default=None)
    age = models.IntegerField( null=True, blank=True)

    # health info 
    blood_type = models.CharField(
        max_length=50, choices=blood_types, null=True, blank=True,default="Not defined")
    diabetes = models.BooleanField( default=False, null=True, blank=True)
    diabetes_type = models.CharField(max_length=50,default=None, choices=diabetes_types, null=True, blank=True)
    blood_preasure = models.BooleanField(default=False, null=True, blank=True)
    diseases = models.TextField(default='No Diseases',null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class secretary(models.Model):
    user=models.OneToOneField(User, related_name="secretary", on_delete=models.CASCADE)
    
    # presonal info
    genders = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(
        max_length=50, choices=genders, default='Male', null=True, blank=True)
    image=models.ImageField(upload_to='photos/doctors/%y%m%d',default=None,null=True,blank=True)

    address = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.IntegerField( null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    working_hours = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

class login_form(models.Model):
    characters=[
        ('doctor', 'doctor'),
        ('patient', 'patient'),
        ('admin','admin'),
        ('secretary', 'secretary'),
    ]
    character = models.CharField(max_length=50,default='patient')
    username=models.CharField( max_length=50)
    password=models.CharField( max_length=50)
# make relation between secreatry and reports
# merge appiontment and report in ERD
class report_appiontment(models.Model):
    date = models.DateField( auto_now=False, auto_now_add=False,default=None,null=True,blank=True)
    time = models.TimeField(auto_now=False, auto_now_add=False,default=None,null=True,blank=True)
    report = models.TextField( null=True, blank=True,default='Not Writen yet')
    doc = models.ForeignKey(doctor, on_delete=models.CASCADE,null=True,blank=True,related_name='patients' )
    patient = models.ForeignKey(patient, on_delete=models.CASCADE, null=True, blank=True,related_name='doctors')
    cost=models.DecimalField(max_digits=8, decimal_places=2,default=None,null=True,blank=True)
    result = models.TextField(null=True, blank=True, default='Not Writen yet')
    drugs = models.TextField(null=True, blank=True, default='Not Writen yet')
    symptoms=models.TextField(null=True, blank=True,default='Not Writen yet')
    done=models.BooleanField(default=False)
    def __str__(self):
        return str(self.patient)
    class Meta:
        unique_together =['date','time','doc']
    
    # edit relation between schedual and doctor => to report_appiontment
class schedule(models.Model):
    report = models.ForeignKey(report_appiontment, on_delete=models.PROTECT)
    def __str__(self):
        return self.report
    

