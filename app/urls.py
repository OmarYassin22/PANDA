from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.Patients,name='patients'),
    path('patients',views.Patients,name='patients'),
    path('patients/<int:id>',views.Patients_id,name='patients_id'),
    path('reports',views.Reports,name='reports'),
    path('reports/<int:id>',views.Reports_id,name='reports'),
    path('secretary',views.Secretary.as_view(),name='secretary'),
    path('secretary/<int:id>',views.Secretary_id.as_view(),name='secretary_id'),
    path('doctors',views.Doctors.as_view(),name='doctors'),
    path('doctors/<int:id>',views.Doctors_id.as_view(),name='doctors_id'),
]

# urlpatterns = [
#     # path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
#     # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
#     # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
#     # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="passwword_reset_complete"),
#     # path('change_password/<token>/',views.change_password,name='change_password'),
#     path('',views.index,name='index'),
#     path('about',views.about,name='about'),
#     path('service',views.service,name='service'),
#     path('feature',views.feature,name='feature'),
#     path('team',views.team,name='team'),
#     path('contact',views.contact,name='contact'),
#     path('appiontment/<int:id>',views.appiontment,name='appiontment'),
#     path('test',views.test,name='test'),
#     path('pf/<int:id>',views.pf,name='pf'),
    
#     path('sec',views.sec,name='sec'),
#     path('sec/sec_patient_search',views.sec_patient_search,name='sec_patient_search'),
#     path('sec/sec_doctor_search',views.sec_doctor_search,name='sec_doctor_search'),
#     path('sec/patients', views.sec_patients, name='sec_patients'),
#     path('sec/doctors', views.sec_doctors, name='sec_doctors'),
#     path('sec/edit_docs/<int:id>', views.edit_docs, name='edit_docs'),
#     path('sec/edit_patients/<int:id>', views.edit_patients, name='edit_patients'),
#     path('sec/delete_pat/<int:id>', views.delete_pat, name='delete_pat'),
#     path('mr',views.mr,name='mr'),
#     path('doctor_info',views.doctor_info,name='doctor_info'),
#     path('signup',views.signup,name='signup'),
#     path('login', views.login, name='login'),
#     path('doc/doctor_sched/<int:id>', views.doctor_sched, name='doctor_sched'),
#     path('doc/doc_profile/<int:id>', views.doc_profile, name='doc_profile'),
#     path('sec/doc_edit_patient/<int:id>', views.doc_edit_patient, name='doc_edit_patient'),
# ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
