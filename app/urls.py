from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.Patients,name='patients'),
    path('patients',views.Patients,name='patients'),
    path('patients/<int:id>',views.Patients_id,name='patients_id'),
    path('reports',views.reports.as_view(),name='reports'),
    path('reports/',views.filter_rep.as_view(),name='reports'),
    path('reports/<int:pk>',views.reports_id.as_view(),name='reports'),
    path('secretary',views.Secretary.as_view(),name='secretary'),
    path('secretary/<int:id>',views.Secretary_id.as_view(),name='secretary_id'),
    path('doctors',views.Doctors.as_view(),name='doctors'),
    path('doctors/<int:id>',views.Doctors_id.as_view(),name='doctors_id'),
    path('doctors/<int:id>/patients',views.doctor_patients.as_view(),name='doctors_id'),
    path('doctors/<int:id>/reports',views.doctor_reports.as_view(),name='doctors_id'),
]

