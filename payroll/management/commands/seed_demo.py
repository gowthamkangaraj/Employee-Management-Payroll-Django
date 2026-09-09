from django.core.management.base import BaseCommand
from payroll.models import Department, Employee
from datetime import date
from decimal import Decimal

class Command(BaseCommand):
    help="Create demo departments and employee if they do not exist."
    def handle(self,*args,**kwargs):
        departments=[("IT","Information Technology"),("HR","Human Resources"),("Finance","Finance and Accounts"),("Marketing","Marketing Department"),("Sales","Sales Department")]
        for n,d in departments: Department.objects.get_or_create(department_name=n,defaults={"description":d})
        it=Department.objects.get(department_name="IT")
        emp,created=Employee.objects.get_or_create(employee_code="EMP1001",defaults={"first_name":"Arun","last_name":"Kumar","email":"arun@gmail.com","phone":"9876543210","gender":"Male","date_of_birth":date(2002,5,15),"address":"Chennai, Tamil Nadu","department":it,"designation":"Software Developer","joining_date":date(2026,1,10),"basic_salary":Decimal("40000"),"status":"Active"})
        self.stdout.write(self.style.SUCCESS("Demo data ready. Employee EMP1001 exists."))
