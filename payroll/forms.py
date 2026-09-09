from django import forms
from .models import Employee, Department, Attendance, Leave, Payroll

class DateInput(forms.DateInput):
    input_type = "date"

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["employee_code","first_name","last_name","email","phone","gender","date_of_birth","address","department","designation","joining_date","basic_salary","status"]
        widgets = {"date_of_birth": DateInput(), "joining_date": DateInput()}

class DepartmentForm(forms.ModelForm):
    class Meta: model = Department; fields = ["department_name","description"]

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance; fields = ["employee","attendance_date","status"]; widgets = {"attendance_date": DateInput()}

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave; fields = ["employee","leave_type","start_date","end_date","reason"]; widgets = {"start_date": DateInput(),"end_date": DateInput()}
    def clean(self):
        data = super().clean()
        if data.get("start_date") and data.get("end_date") and data["end_date"] < data["start_date"]:
            raise forms.ValidationError("End date cannot be before start date.")
        return data

class PayrollForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.filter(status="Active"))
    payroll_month = forms.DateField(widget=DateInput(), help_text="Use the first day of the month, e.g. 2026-09-01")
    bonus = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, initial=0, required=False)
    allowances = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, initial=0, required=False)
    tax = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, initial=0, required=False)
    other_deductions = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, initial=0, required=False)
    unpaid_leave_days = forms.IntegerField(min_value=0, initial=0, required=False)
    def clean_payroll_month(self):
        d = self.cleaned_data["payroll_month"]
        if d.day != 1: raise forms.ValidationError("Payroll month must be the first day of the month.")
        return d
