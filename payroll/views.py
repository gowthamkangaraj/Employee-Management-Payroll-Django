import csv
from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum, Avg, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmployeeForm, DepartmentForm, AttendanceForm, LeaveForm, PayrollForm
from .models import Employee, Department, Attendance, Leave, Payroll
from .services import calculate_salary

@login_required
def dashboard(request):
    context={"employee_count":Employee.objects.filter(status="Active").count(),"department_count":Department.objects.count(),"pending_leaves":Leave.objects.filter(status="Pending").count(),"payroll_count":Payroll.objects.count(),"recent_payroll":Payroll.objects.select_related("employee").order_by("-generated_at")[:5]}
    return render(request,"payroll/dashboard.html",context)

@login_required
def employees(request):
    q=request.GET.get("q","").strip(); qs=Employee.objects.select_related("department").all()
    if q: qs=qs.filter(Q(employee_code__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(email__icontains=q)|Q(designation__icontains=q))
    return render(request,"payroll/employees.html",{"employees":qs,"q":q})

@login_required
def employee_create(request):
    form=EmployeeForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,"Employee added successfully."); return redirect("employees")
    return render(request,"payroll/form.html",{"form":form,"title":"Add Employee","back":"employees"})

@login_required
def employee_edit(request,pk):
    obj=get_object_or_404(Employee,pk=pk); form=EmployeeForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,"Employee updated successfully."); return redirect("employees")
    return render(request,"payroll/form.html",{"form":form,"title":"Update Employee","back":"employees"})

@login_required
def employee_delete(request,pk):
    obj=get_object_or_404(Employee,pk=pk)
    if request.method=="POST": obj.delete(); messages.success(request,"Employee deleted.")
    return redirect("employees")

@login_required
def departments(request): return render(request,"payroll/departments.html",{"departments":Department.objects.annotate(employee_count=Count("employees"))})

@login_required
def department_create(request):
    form=DepartmentForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,"Department added."); return redirect("departments")
    return render(request,"payroll/form.html",{"form":form,"title":"Add Department","back":"departments"})

@login_required
def department_edit(request,pk):
    obj=get_object_or_404(Department,pk=pk); form=DepartmentForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,"Department updated."); return redirect("departments")
    return render(request,"payroll/form.html",{"form":form,"title":"Update Department","back":"departments"})

@login_required
def department_delete(request,pk):
    obj=get_object_or_404(Department,pk=pk)
    if request.method=="POST": obj.delete(); messages.success(request,"Department deleted.")
    return redirect("departments")

@login_required
def attendance(request):
    form=AttendanceForm(request.POST or None)
    if form.is_valid():
        obj,created=Attendance.objects.update_or_create(employee=form.cleaned_data["employee"],attendance_date=form.cleaned_data["attendance_date"],defaults={"status":form.cleaned_data["status"]}); messages.success(request,"Attendance saved."); return redirect("attendance")
    records=Attendance.objects.select_related("employee").all()[:100]
    return render(request,"payroll/attendance.html",{"form":form,"records":records})

@login_required
def attendance_summary(request):
    month=request.GET.get("month",date.today().strftime("%Y-%m")); rows=[]
    try:
        y,m=map(int,month.split("-")); rows=Attendance.objects.filter(attendance_date__year=y,attendance_date__month=m).values("employee__employee_code","employee__first_name","employee__last_name","status").annotate(count=Count("attendance_id")).order_by("employee__employee_code","status")
    except ValueError: messages.error(request,"Invalid month. Use YYYY-MM.")
    return render(request,"payroll/attendance_summary.html",{"rows":rows,"month":month})

@login_required
def leaves(request):
    form=LeaveForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,"Leave application submitted."); return redirect("leaves")
    records=Leave.objects.select_related("employee").all()
    return render(request,"payroll/leaves.html",{"form":form,"leaves":records})

@login_required
def leave_status(request,pk):
    obj=get_object_or_404(Leave,pk=pk)
    if request.method=="POST":
        status=request.POST.get("status")
        if status in {"Approved","Rejected"}: obj.status=status; obj.save(update_fields=["status"]); messages.success(request,f"Leave {status.lower()}.")
    return redirect("leaves")

@login_required
def payroll(request):
    form=PayrollForm(request.POST or None)
    if form.is_valid():
        d=form.cleaned_data; s=calculate_salary(d["employee"].basic_salary,allowances=d.get("allowances") or 0,bonus=d.get("bonus") or 0,tax=d.get("tax") or 0,other_deductions=d.get("other_deductions") or 0,leave_days=d.get("unpaid_leave_days") or 0)
        with transaction.atomic():
            obj,created=Payroll.objects.update_or_create(employee=d["employee"],payroll_month=d["payroll_month"],defaults={"basic_salary":s["basic"],"hra":s["hra"],"allowances":s["allowances"],"bonus":s["bonus"],"gross_salary":s["gross"],"pf":s["pf"],"tax":s["tax"],"other_deductions":s["other_deductions"],"leave_deduction":s["leave_deduction"],"total_deductions":s["total_deductions"],"net_salary":s["net"]})
        messages.success(request,f"Payroll {'generated' if created else 'updated'}. Net salary: ₹{s['net']:,.2f}"); return redirect("payroll")
    records=Payroll.objects.select_related("employee").all()
    return render(request,"payroll/payroll.html",{"form":form,"records":records})

@login_required
def payroll_detail(request,pk): return render(request,"payroll/payroll_detail.html",{"record":get_object_or_404(Payroll.objects.select_related("employee"),pk=pk)})

@login_required
def reports(request):
    month=request.GET.get("month",date.today().strftime("%Y-%m")); qs=Payroll.objects.select_related("employee");
    try: y,m=map(int,month.split("-")); qs=qs.filter(payroll_month__year=y,payroll_month__month=m)
    except ValueError: messages.error(request,"Invalid month. Use YYYY-MM.")
    totals=qs.aggregate(records=Count("payroll_id"),gross=Sum("gross_salary"),deductions=Sum("total_deductions"),net=Sum("net_salary"),average=Avg("net_salary"))
    return render(request,"payroll/reports.html",{"month":month,"records":qs,"totals":totals})

@login_required
def export_csv(request):
    month=request.GET.get("month",date.today().strftime("%Y-%m")); response=HttpResponse(content_type="text/csv"); response["Content-Disposition"]=f'attachment; filename="payroll_{month}.csv"'; writer=csv.writer(response); writer.writerow(["Employee Code","Employee Name","Month","Gross Salary","Deductions","Net Salary"]);
    try: y,m=map(int,month.split("-")); qs=Payroll.objects.select_related("employee").filter(payroll_month__year=y,payroll_month__month=m)
    except ValueError: qs=Payroll.objects.none()
    for p in qs: writer.writerow([p.employee.employee_code,p.employee.first_name+" "+(p.employee.last_name or ""),p.payroll_month.strftime("%Y-%m"),p.gross_salary,p.total_deductions,p.net_salary])
    return response
