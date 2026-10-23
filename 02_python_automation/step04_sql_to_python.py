# ==============================================================================
# 🔰 အဆင့် (၄): SQL DATABASE နှင့် PYTHON ကို တိုက်ရိုက် ချိတ်ဆက်ခြင်း
# ==============================================================================

import sqlite3
import pandas as pd

# ၁။ Database သို့ ချိတ်ဆက်မှု လှမ်းဖွင့်ခြင်း (Connect to Database)
DB_PATH = "data/hr_payroll.db"
conn = sqlite3.connect(DB_PATH)

print("=" * 85)
print("✅ ၁။ Database သို့ အောင်မြင်စွာ ချိတ်ဆက်ပြီးပါပြီ!")
print("=" * 85)

# ၂။ SQL Query ရေးသားခြင်း:
# Employees table နှင့် Payroll table ကို JOIN တွဲပြီး
# ဌာနအလိုက် Overtime စရိတ်နှင့် စုစုပေါင်း လစာ ကုန်ကျစရိတ်ကို Database တွင် တိုက်ရိုက် တွက်ခိုင်းခြင်း
sql_query = """
SELECT 
    e.department AS Department,
    COUNT(DISTINCT e.emp_id) AS Headcount,
    ROUND(SUM(p.ot_hours), 1) AS Total_OT_Hours,
    PRINTF('%,d MMK', SUM(p.ot_pay)) AS Total_OT_Cost,
    PRINTF('%,d MMK', SUM(p.gross_salary)) AS Total_Gross_Payroll
FROM payroll_records p
JOIN employees e ON p.emp_id = e.emp_id
GROUP BY e.department
ORDER BY SUM(p.ot_hours) DESC;
"""

# ၃။ SQL Query ကို Database ထံ ပို့ပြီး ရလဒ်ကို Python DataFrame အဖြစ် တိုက်ရိုက် ဖတ်ယူခြင်း
df_payroll_summary = pd.read_sql_query(sql_query, conn)

print("📊 Database မှ တိုက်ရိုက် ရရှိလာသော ဌာနအလိုက် Payroll & OT ကုန်ကျစရိတ် ဇယား:")
print(df_payroll_summary)
print("=" * 85)

# ၄။ အလုပ်ပြီးပါက Database Connection ကို သော့ပြန်ပိတ်ခြင်း
conn.close()
print("🔒 Database Connection ကို စနစ်တကျ ပိတ်သိမ်းပြီးပါပြီ။")
