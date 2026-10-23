import sqlite3
import pandas as pd
from datetime import datetime

# Database မှ Data ဖတ်ယူခြင်း
conn = sqlite3.connect("data/hr_payroll.db")

# 1. Employees Table
df_emp = pd.read_sql_query("SELECT * FROM employees;", conn)

# Calculate Years of Service (လက်ရှိရက်အထိ လုပ်သက်တွက်ခြင်း)
ref_date = datetime(2026, 10, 1)
df_emp['hire_date_dt'] = pd.to_datetime(df_emp['hire_date'])
df_emp['years_of_service'] = ((ref_date - df_emp['hire_date_dt']).dt.days / 365.25).round(1)
df_emp.drop(columns=['hire_date_dt'], inplace=True)

# 2. Payroll Monthly History Table
df_payroll = pd.read_sql_query("SELECT * FROM payroll_records;", conn)

conn.close()

# Export to Multi-tab Excel file designed specifically for Power BI Star Schema
excel_output = "data/PowerBI_HR_Workforce_Dataset.xlsx"
with pd.ExcelWriter(excel_output, engine="openpyxl") as writer:
    df_emp.to_excel(writer, sheet_name="Dim_Employees", index=False)
    df_payroll.to_excel(writer, sheet_name="Fact_Payroll_History", index=False)

print(f"✅ Power BI အတွက် အသင့်သုံးနိုင်သော Excel Dataset ကို '{excel_output}' သို့ ထုတ်ပေးပြီးပါပြီ!")
print(f"📊 Sheet 1: 'Dim_Employees' ({len(df_emp)} rows)")
print(f"📊 Sheet 2: 'Fact_Payroll_History' ({len(df_payroll)} rows)")
