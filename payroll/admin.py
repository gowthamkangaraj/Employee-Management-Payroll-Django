from django.contrib import admin
from .models import Department, Employee, Attendance, Leave, Payroll
admin.site.register([Department,Employee,Attendance,Leave,Payroll])
