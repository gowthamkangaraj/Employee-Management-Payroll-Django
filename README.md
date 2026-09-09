# Employee Management & Payroll System — Django Web Application

A web-based version of the Employee Management & Payroll System, built with **Python, Django, MySQL, and Pandas-ready reporting workflows**. It converts the original console application into a browser-accessible application while keeping the same core business modules.

## Features
- Admin login using Django authentication
- Employee CRUD and search
- Department CRUD
- Attendance marking and monthly summary
- Leave application and approval/rejection
- Payroll generation with HRA, PF, tax, other deductions, and unpaid-leave deduction
- Monthly payroll reports
- CSV export
- Django Admin interface
- Environment variables for secrets and database credentials

## Tech Stack
- Python 3.13+
- Django
- MySQL
- PyMySQL
- python-dotenv
- Bootstrap 5

## Windows Setup
1. Extract this ZIP.
2. Open the folder in VS Code.
3. Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```
4. Install dependencies:
```powershell
pip install -r requirements.txt
```
5. Create `.env` from `.env.example` and enter your MySQL credentials.
6. Make sure the existing `employee_payroll` database/schema is available. The original SQL schema is included as `schema_existing.sql`.
7. Create Django's authentication/admin tables:
```powershell
python manage.py migrate
```
8. Create an administrator:
```powershell
python manage.py createsuperuser
```
9. Optional demo data:
```powershell
python manage.py seed_demo
```
10. Start the website:
```powershell
python manage.py runserver
```
11. Open **http://127.0.0.1:8000/**

## Payroll Formula
Gross = Basic + HRA (40% of Basic) + Allowances + Bonus

Deductions = PF (12% of Basic) + Tax + Other Deductions + Unpaid Leave Deduction

Net = Gross − Total Deductions

Unpaid leave deduction uses Gross / 26 working days × unpaid leave days.

## Deployment
For public access, deploy the Django application to a cloud platform and use a managed MySQL database. Before deployment, set `DEBUG=False`, configure `ALLOWED_HOSTS`, use a strong `SECRET_KEY`, and never upload `.env` or real database passwords to GitHub.

## Original Project
This Django version was created from the original Employee Management & Payroll System console application's modules and database design.
