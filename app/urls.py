from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.authtoken import views as auth_view

from rest_framework.routers import DefaultRouter
router =DefaultRouter()
# router.register('reports',views.report_viewset)

urlpatterns = [
    path('',views.ListPatients.as_view()),

    # path('',views.Patients,name='patients'),
    # path('patients/',views.Patients,name='patients'),
    # path('patients/<int:id>',views.Patients_id,name='patients_id'),
    path('patient/reports',views.patient_reports.as_view(),name='reports'),
    path('reports/',views.filter_rep.as_view(),name='reports'),
    path('reports/<int:pk>',views.reports_id.as_view(),name='reports'),
    path('secretary',views.Secretary.as_view(),name='secretary'),
    path('secretary/<int:id>',views.Secretary_id.as_view(),name='secretary_id'),
    path('doctors_list/',views.doctor_list.as_view()),
    path('doctor/',views.Doctors_id.as_view(),name='doctors_id'),
    path('doctor/patients',views.doctor_patients.as_view(),name='doctors_id'),
    path('doctor/reports',views.doctor_reports.as_view(),name='doctors_id'),
    path('patient_profile',views.patient_view.as_view(),name='patient_profile'),
    path('signup/patients/',views.signup_patients.as_view()),
    path('patient/',views.PatientProfile.as_view()),
    path('patient/edit/',views.PatientProfileEdite.as_view()),
    path('signup/doctors/',views.signup_doctors.as_view()),
    path('signup/doctors/continue',views.signup_doctors_info.as_view()),
    path('patient/doctors/',views.ListDoctors.as_view()),
    path('login/',views.log_in.as_view(),name="auth_token"),
    path('logout/',views.log_out.as_view(), name='logout'),
    path('signup/secretaries/',views.signup_secretaries.as_view()),
    path('secretaries/',views.ListSecretaries.as_view()),

    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),





]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

