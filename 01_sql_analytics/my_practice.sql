-- ==============================================================================
-- ✍️ MY SQL PRACTICE (လက်တွေ့ စမ်းသပ်လေ့ကျင့်ရန် နေရာ)
-- Runner: python 01_sql_analytics/run_query.py 01_sql_analytics/my_practice.sql
-- ==============================================================================

-- 📌 မေးခွန်း (A): "Finance" ဌာနမှ Active ဝန်ထမ်းများ၏ name, job_title, base_salary ကို ရှာဖွေပါ
-- သင့်ရဲ့ Query ကို အောက်မှာ ရေးပါ 👇:



-- 📌 မေးခွန်း (B): "Sales" ဌာနမှ လစာ ၁၂ သိန်းနှင့်အထက် ရရှိသော Active ဝန်ထမ်း ဦးရေကို ရှာဖွေပါ
-- သင့်ရဲ့ Query ကို အောက်မှာ ရေးပါ 👇:
SELECT
COUNT(*) As total_employees
From employees
Where department = 'Finance'
AND base_salary < 1500000
AND employment_status = 'Active';
Select education , AVG(base_salary)
From employees
WHERE employment_status = 'Active'
GROUP BY education;

