from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    class Meta: db_table = "departments"
    def __str__(self): return self.department_name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=120, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, db_column="department_id", on_delete=models.SET_NULL, blank=True, null=True, related_name="employees")
    designation = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField()
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=8, choices=[("Active","Active"),("Inactive","Inactive")], default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = "employees"
    def __str__(self): return f"{self.employee_code} - {self.first_name} {self.last_name or ''}".strip()

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, db_column="employee_id", on_delete=models.CASCADE, related_name="attendance")
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=[("Present","Present"),("Absent","Absent"),("Half Day","Half Day"),("Leave","Leave")])
    class Meta:
        db_table = "attendance"
        constraints = [models.UniqueConstraint(fields=["employee","attendance_date"], name="uq_attendance_django")]
        ordering = ["-attendance_date"]

class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, db_column="employee_id", on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.CharField(max_length=10, choices=[("Casual","Casual"),("Sick","Sick"),("Earned","Earned"),("Unpaid","Unpaid")])
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=8, choices=[("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = "leaves"; ordering = ["-created_at"]

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, db_column="employee_id", on_delete=models.CASCADE, related_name="payrolls")
    payroll_month = models.DateField()
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    pf = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    leave_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = "payroll"; constraints = [models.UniqueConstraint(fields=["employee","payroll_month"], name="uq_payroll_django")]; ordering = ["-payroll_month"]
