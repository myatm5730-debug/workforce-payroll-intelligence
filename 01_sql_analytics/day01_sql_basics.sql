-- ==============================================================================
-- 🎯 DAY 1: SQL BASICS & PAYROLL DATA EXTRACTION
-- Database: data/hr_payroll.db
-- Runner: python 01_sql_analytics/run_query.py 01_sql_analytics/day01_sql_basics.sql
-- ==============================================================================

-- 📌 Question 1: လက်ရှိ တာဝန်ထမ်းဆောင်နေသော Active ဝန်ထမ်းများ၏ ဌာနအလိုက် Headcount နှင့် ပျမ်းမျှလစာ
SELECT 
    department,
    COUNT(emp_id) AS total_headcount,
    PRINTF('%,d MMK', CAST(AVG(base_salary) AS INT)) AS avg_salary,
    PRINTF('%,d MMK', MIN(base_salary)) AS min_salary,
    PRINTF('%,d MMK', MAX(base_salary)) AS max_salary
FROM employees
WHERE employment_status = 'Active'
GROUP BY department
ORDER BY AVG(base_salary) DESC;

-- 📌 Question 2: လစာ ၁,၅၀၀,၀၀၀ MMK အထက်ရရှိသော အဆင့်မြင့်ဝန်ထမ်းများ စာရင်း
SELECT 
    emp_id,
    name,
    department,
    job_title,
    PRINTF('%,d MMK', base_salary) AS base_salary,
    performance_rating
FROM employees
WHERE base_salary >= 1500000 
  AND employment_status = 'Active'
ORDER BY base_salary DESC
LIMIT 10;

-- 📌 Question 3: လစာစာရင်း (Payroll) မှ Overtime အများဆုံး ဆင်းရသော Top 10 ဝန်ထမ်းများ
SELECT 
    p.payroll_date,
    p.emp_id,
    e.name,
    e.department,
    p.ot_hours,
    PRINTF('%,d MMK', p.ot_pay) AS ot_pay,
    PRINTF('%,d MMK', p.net_salary) AS net_salary
FROM payroll_records p
JOIN employees e ON p.emp_id = e.emp_id
WHERE p.payroll_date = '2026-09-30'
ORDER BY p.ot_hours DESC
LIMIT 10;

-- ==============================================================================
-- 📌 Challenge 1 (Your Turn): 
-- မေးခွန်း: ၂၀၂၃ ခုနှစ် နောက်ပိုင်းမှ အလုပ်စဝင်ခဲ့ပြီး (hire_date >= '2023-01-01')
--          လက်ရှိ အခြေခံလစာ ၁၀ သိန်းအောက် ရနေသော (base_salary < 1000000)
--          Active ဝန်ထမ်းများ၏ အရေအတွက်နှင့် အချက်အလက်များကို ရှာဖွေပါ။
-- ==============================================================================

-- သင့်ရဲ့ SQL Query ကို ဒီအောက်မှာ ရေးကြည့်ပါ 👇:
SELECT 
    department,
    COUNT(emp_id) AS total_headcount,
    PRINTF('%,d MMK', CAST(AVG(base_salary) AS INT)) AS avg_salary,
    PRINTF('%,d MMK', MIN(base_salary)) AS min_salary,
    PRINTF('%,d MMK', MAX(base_salary)) AS max_salary
FROM employees
WHERE employment_status = 'Active'
GROUP BY department
ORDER BY AVG(base_salary) DESC;



