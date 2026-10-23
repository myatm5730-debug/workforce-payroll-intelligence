import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 Hands-On Data Analytics Lab: SQL, Python, Pivot Table & Power BI\n",
    "ဒီ Notebook ထဲမှာ သင့်အနေနဲ့ Cell တစ်ခုချင်းစီကို **`Shift + Enter`** သို့မဟုတ် **`▶ Run`** ခလုတ် နှိပ်ပြီး ချက်ချင်း အဖြေဇယားနှင့် Chart များကို မျက်စိနဲ့ တပ်အပ် မြင်တွေ့ရမှာ ဖြစ်ပါတယ်။"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## အဆင့် (၁) - Database (SQL) နှင့် ချိတ်ဆက်ပြီး Data ဆွဲယူခြင်း"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlite3\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "# Database နှင့် ချိတ်ဆက်ခြင်း\n",
    "conn = sqlite3.connect('data/hr_payroll.db')\n",
    "\n",
    "# SQL ဖြင့် Employees Data ဆွဲထုတ်ခြင်း\n",
    "query = '''\n",
    "SELECT emp_id, name, gender, department, job_title, base_salary, hire_date, employment_status, performance_rating\n",
    "FROM employees;\n",
    "'''\n",
    "df_emp = pd.read_sql_query(query, conn)\n",
    "print('Data Loaded Successfully! Total Rows:', len(df_emp))\n",
    "df_emp.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## အဆင့် (၂) - Python တွင် Excel Pivot Table ကဲ့သို့ အုပ်စုဖွဲ့ တွက်ချက်ခြင်း (`df.pivot_table`)\n",
    "**Excel မှာ Pivot Table ဆွဲသလိုမျိုး** ဌာနအလိုက် (`Index`)၊ ကျား/မ အလိုက် (`Columns`)၊ ပျမ်းမျှလစာကို တွက်ချက်ပြခြင်း:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Excel Pivot Table in Python\n",
    "pivot_salary = df_emp[df_emp['employment_status'] == 'Active'].pivot_table(\n",
    "    index='department',\n",
    "    columns='gender',\n",
    "    values='base_salary',\n",
    "    aggfunc=['count', 'mean']\n",
    ")\n",
    "\n",
    "# Format numbers nicely\n",
    "pivot_salary"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## အဆင့် (၃) - SQL + Payroll Analysis: Overtime (OT) အများဆုံး ဌာနများ စစ်ဆေးခြင်း"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "query_ot = '''\n",
    "SELECT \n",
    "    e.department,\n",
    "    ROUND(SUM(p.ot_hours), 1) AS total_ot_hours,\n",
    "    PRINTF('%,d MMK', SUM(p.ot_pay)) AS total_ot_cost,\n",
    "    PRINTF('%,d MMK', SUM(p.gross_salary)) AS total_gross_payroll\n",
    "FROM payroll_records p\n",
    "JOIN employees e ON p.emp_id = e.emp_id\n",
    "GROUP BY e.department\n",
    "ORDER BY SUM(p.ot_hours) DESC;\n",
    "'''\n",
    "df_ot = pd.read_sql_query(query_ot, conn)\n",
    "df_ot"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## အဆင့် (၄) - Power BI သို့မဟုတ် Excel ထဲသို့ တိုက်ရိုက် သွင်းနိုင်ရန် Export ထုတ်ခြင်း"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Cleaned & aggregated data ကို Excel/CSV အဖြစ် ထုတ်ပေးခြင်း\n",
    "df_emp.to_excel('data/Cleaned_HR_Employees.xlsx', index=False)\n",
    "print('✅ data/Cleaned_HR_Employees.xlsx သို့ Export ထုတ်ပြီးပါပြီ။ Power BI သို့မဟုတ် Excel တွင် ချက်ချင်း ဖွင့်နိုင်ပါပြီ!')\n",
    "conn.close()"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("01_Data_Analytics_Lab.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print("Notebook created successfully!")
