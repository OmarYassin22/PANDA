from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(secretary)
admin.site.register(schedule)
admin.site.register(report_appiontment)

