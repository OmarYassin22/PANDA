from django.db import models
from django import forms

from django.contrib.auth.models import User
# Create your models here.
class doctor(models.Model):
    # presonal info
    genders = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
   

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=genders, default='Male',null=True,blank=True)
    address = models.CharField(max_length=50, null=True, blank=True,default="There is No Address for communication ")
    username = models.CharField(max_length=254, null=True, blank=True)
    phone_number = models.IntegerField( null=True, blank=True)
    password = models.CharField(max_length=150, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)




    def __str__(self):
        return self.name
    class Meta:
        unique_together=['username']
    

class patient( models.Model):
    # presonal info
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
    diabete_types=[
        ('type 1', 'type 1'),
        ('type 2', 'type 2')
    ]
    payments = [
        ('cash', 'cash'),
        ('VISA', 'VISA')
    ]
    
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=genders,default="Male",null=True,blank=True )
    address = models.CharField(max_length=50, null=True, blank=True,default="There is no current address")
    username = models.CharField(  max_length=50)
    email = models.EmailField(max_length=254,null=True, blank=True, default=None)
    phone_number = models.IntegerField( null=True, blank=True,default='None')
    password = models.CharField( max_length=150)
    age = models.IntegerField( null=True, blank=True)
    

    # health info 
    blood_type = models.CharField(
        max_length=50, choices=blood_types, null=True, blank=True,default="Not defined")
    diabete = models.BooleanField( default=None, null=True, blank=True)
    diabete_type = models.CharField(max_length=50,default="Not defined", choices=diabete_types, null=True, blank=True)
    blood_presure = models.BooleanField(default=False, null=True, blank=True)
    diseases = models.TextField(default='No Diseases',null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        unique_together=['username']
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

    
class report_appiontment(models.Model): 
    doc = models.ForeignKey(
        doctor, on_delete=models.DO_NOTHING,null=True,blank=True)
    patient = models.ForeignKey(
        patient, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField( auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    report = models.TextField( null=True, blank=True,default='Not Writen yet')
    symptoms=models.TextField(null=True, blank=True,default='Not Writen yet')
    result = models.TextField(null=True, blank=True, default='Not Writen yet')
    drugs = models.TextField(null=True, blank=True, default='Not Writen yet')
    cost=models.DecimalField(max_digits=8, decimal_places=2,default=0)
    done=models.BooleanField(default=False)
    def __str__(self):
        return str(self.patient)
    class Meta:
        unique_together =['date','time']
    

class secretary(models.Model):
    # presonal info
    genders = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=50, choices=genders, default='Male', null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50)
    phone_number = models.IntegerField( null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=150)
    working_hours = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        unique_together=['username']

class schedule(models.Model):
    report = models.ForeignKey(report_appiontment, on_delete=models.PROTECT)
    def __str__(self):
        return self.report

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token= models.CharField( max_length=100)
    created_at=models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.user.username

    
