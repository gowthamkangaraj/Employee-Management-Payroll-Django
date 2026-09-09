from django.urls import path
from . import views
urlpatterns=[
 path("",views.dashboard,name="dashboard"), path("employees/",views.employees,name="employees"), path("employees/add/",views.employee_create,name="employee_create"), path("employees/<int:pk>/edit/",views.employee_edit,name="employee_edit"), path("employees/<int:pk>/delete/",views.employee_delete,name="employee_delete"),
 path("departments/",views.departments,name="departments"), path("departments/add/",views.department_create,name="department_create"), path("departments/<int:pk>/edit/",views.department_edit,name="department_edit"), path("departments/<int:pk>/delete/",views.department_delete,name="department_delete"),
 path("attendance/",views.attendance,name="attendance"), path("attendance/summary/",views.attendance_summary,name="attendance_summary"), path("leaves/",views.leaves,name="leaves"), path("leaves/<int:pk>/status/",views.leave_status,name="leave_status"),
 path("payroll/",views.payroll,name="payroll"), path("payroll/<int:pk>/",views.payroll_detail,name="payroll_detail"), path("reports/",views.reports,name="reports"), path("reports/export/",views.export_csv,name="export_csv"),
]
