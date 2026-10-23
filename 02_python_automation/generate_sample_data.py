import os
import random
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

first_names = [
    "Aung", "Kyaw", "Min", "Thura", "Zayar", "Ko", "Myo", "Tin", "Htet", "Wai",
    "Su", "Thandar", "Hnin", "Aye", "Phyu", "May", "Khin", "Yamin", "Ei", "Nilar",
    "Zaw", "Bo", "Naing", "Soe", "Thet", "Yin", "Mon", "Sandar", "Mya", "Win"
]
last_names = [
    "Ko", "Lwin", "Oo", "Tun", "Zaw", "Aung", "Moe", "Naing", "Swe", "Kyaw",
    "San", "Hlaing", "Win", "Myint", "Htun", "Khaing", "Nwe", "Aye", "Thu", "Thant"
]

departments = ["HR", "Finance", "Sales", "Operations", "Engineering", "Marketing"]
roles_by_dept = {
    "HR": [("HR Assistant", 600000), ("HR Officer", 900000), ("HR Payroll Executive", 1300000), ("HR Manager", 2500000)],
    "Finance": [("Junior Accountant", 650000), ("Accountant", 1000000), ("Finance Analyst", 1500000), ("Finance Manager", 2800000)],
    "Sales": [("Sales Rep", 500000), ("Senior Sales Rep", 850000), ("Account Executive", 1400000), ("Sales Manager", 3000000)],
    "Operations": [("Ops Coordinator", 550000), ("Logistics Specialist", 850000), ("Ops Supervisor", 1200000), ("Ops Manager", 2400000)],
    "Engineering": [("Junior Developer", 900000), ("Software Engineer", 1600000), ("Senior Engineer", 2800000), ("Tech Lead", 4200000)],
    "Marketing": [("Content Creator", 600000), ("Marketing Specialist", 950000), ("Digital Marketing Lead", 1600000), ("Marketing Director", 3500000)]
}

genders = ["Male", "Female"]
employment_types = ["Full-Time", "Contract"]
education_levels = ["Bachelor's", "Master's", "Diploma"]

num_employees = 500
employees = []

start_date = datetime(2021, 1, 1)
end_date = datetime(2026, 9, 30)

for emp_id in range(1001, 1001 + num_employees):
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    full_name = f"{fname} {lname}"
    gender = "Female" if fname in ["Su", "Thandar", "Hnin", "Aye", "Phyu", "May", "Khin", "Yamin", "Ei", "Nilar", "Yin", "Mon", "Sandar"] else "Male"
    
    dept = random.choice(departments)
    role_info = random.choice(roles_by_dept[dept])
    job_title = role_info[0]
    base_salary = int(role_info[1] * random.uniform(0.9, 1.25))
    
    # Hire date between 2021 and 2025
    days_between = (end_date - start_date).days
    hire_date = start_date + timedelta(days=random.randint(0, days_between - 180))
    
    # Attrition simulation (approx 15% resigned)
    is_resigned = random.random() < 0.16
    if is_resigned:
        employment_status = "Resigned"
        exit_days = random.randint(180, (end_date - hire_date).days)
        exit_date = hire_date + timedelta(days=exit_days)
        if exit_date > end_date:
            employment_status = "Active"
            exit_date = None
    else:
        employment_status = "Active"
        exit_date = None
        
    performance_rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.15, 0.50, 0.20, 0.10])[0]
    
    employees.append({
        "emp_id": emp_id,
        "name": full_name,
        "gender": gender,
        "department": dept,
        "job_title": job_title,
        "base_salary": base_salary,
        "hire_date": hire_date.strftime("%Y-%m-%d"),
        "employment_status": employment_status,
        "exit_date": exit_date.strftime("%Y-%m-%d") if exit_date else None,
        "performance_rating": performance_rating,
        "education": random.choice(education_levels),
        "employment_type": random.choices(employment_types, weights=[0.85, 0.15])[0]
    })

df_employees = pd.DataFrame(employees)

# Generate Payroll History (Last 12 months: Oct 2025 - Sep 2026)
payroll_records = []
attendance_records = []

months = [
    "2025-10-31", "2025-11-30", "2025-12-31",
    "2026-01-31", "2026-02-28", "2026-03-31",
    "2026-04-30", "2026-05-31", "2026-06-30",
    "2026-07-31", "2026-08-31", "2026-09-30"
]

for pay_date_str in months:
    pay_date = datetime.strptime(pay_date_str, "%Y-%m-%d")
    
    for emp in employees:
        hire_dt = datetime.strptime(emp["hire_date"], "%Y-%m-%d")
        if hire_dt > pay_date:
            continue
            
        exit_dt = datetime.strptime(emp["exit_date"], "%Y-%m-%d") if emp["exit_date"] else None
        
        # Intentional Audit Anomaly: 2 Resigned employees still paid (Ghost employees)
        if exit_dt and exit_dt < pay_date:
            if emp["emp_id"] not in [1014, 1088]:
                continue
            # Else ghost employee paid!
            
        base = emp["base_salary"]
        ot_hours = round(random.choices([0, random.uniform(5, 20), random.uniform(25, 60)], weights=[0.4, 0.45, 0.15])[0], 1)
        # Sales team has high OT or Ops team
        if emp["department"] in ["Operations", "Sales"] and random.random() < 0.2:
            ot_hours += random.uniform(15, 35)
            
        hourly_rate = base / (22 * 8)
        ot_pay = int(ot_hours * hourly_rate * 1.5)
        
        allowance = 50000 if emp["employment_type"] == "Full-Time" else 20000
        gross_salary = base + ot_pay + allowance
        
        # SSB deduction (2% capped at max SSB limit 300,000 kyat base -> max 6,000 kyats)
        ssb_deduction = min(int(base * 0.02), 6000)
        
        # Income Tax estimation (Myanmar tax tier basic)
        taxable_yearly = gross_salary * 12
        if taxable_yearly > 4800000:
            tax_monthly = int((gross_salary - 400000) * 0.05)
        else:
            tax_monthly = 0
            
        net_salary = gross_salary - ssb_deduction - tax_monthly
        
        payroll_records.append({
            "payroll_id": f"PAY-{pay_date.strftime('%Y%m')}-{emp['emp_id']}",
            "emp_id": emp["emp_id"],
            "payroll_date": pay_date_str,
            "base_salary": base,
            "ot_hours": ot_hours,
            "ot_pay": ot_pay,
            "allowances": allowance,
            "gross_salary": gross_salary,
            "ssb_deduction": ssb_deduction,
            "tax_deduction": tax_monthly,
            "net_salary": net_salary
        })
        
        # Attendance details
        working_days = 22
        leave_days = random.choices([0, 1, 2, 3], weights=[0.6, 0.25, 0.1, 0.05])[0]
        actual_present = working_days - leave_days
        
        attendance_records.append({
            "record_id": f"ATT-{pay_date.strftime('%Y%m')}-{emp['emp_id']}",
            "emp_id": emp["emp_id"],
            "period": pay_date_str[:7],
            "working_days": working_days,
            "days_present": actual_present,
            "leave_days": leave_days,
            "ot_hours": ot_hours
        })

df_payroll = pd.DataFrame(payroll_records)
df_attendance = pd.DataFrame(attendance_records)

# Save to CSV
df_employees.to_csv("data/employees.csv", index=False)
df_payroll.to_csv("data/payroll_records.csv", index=False)
df_attendance.to_csv("data/attendance_ot.csv", index=False)

# Save to SQLite Database
db_path = "data/hr_payroll.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
df_employees.to_sql("employees", conn, if_exists="replace", index=False)
df_payroll.to_sql("payroll_records", conn, if_exists="replace", index=False)
df_attendance.to_sql("attendance_records", conn, if_exists="replace", index=False)

# Create Indexes
cursor = conn.cursor()
cursor.execute("CREATE INDEX idx_emp_id ON employees(emp_id);")
cursor.execute("CREATE INDEX idx_payroll_emp_date ON payroll_records(emp_id, payroll_date);")
cursor.execute("CREATE INDEX idx_attendance_emp_period ON attendance_records(emp_id, period);")
conn.commit()
conn.close()

print(f"Generated {len(df_employees)} employees, {len(df_payroll)} payroll records, {len(df_attendance)} attendance records.")
print(f"Saved CSVs and SQLite Database to {db_path} successfully!")
