-- ==============================================================================
-- 🎯 DAY 2: GROUP BY & AGGREGATIONS (EXCEL PIVOT TABLE IN SQL)
-- Database: data/hr_payroll.db
-- Runner: python 01_sql_analytics/run_query.py 01_sql_analytics/day02_group_by_aggregations.sql
-- ==============================================================================

-- 🔹 ဥပမာ (၁) - ဌာနအလိုက် ဝန်ထမ်းဦးရေ (Headcount) ရှာဖွေခြင်း
SELECT 
    department,
    COUNT(*) AS headcount
FROM employees
WHERE employment_status = 'Active'
GROUP BY department
ORDER BY headcount DESC;

-- 🔹 ဥပမာ (၂) - ဌာနအလိုက် လစာ ကုန်ကျစရိတ် စုစုပေါင်း (Total Payroll Budget) နှင့် ပျမ်းမျှလစာ
-- PRINTF('%,d MMK', ...) သည် ဂဏန်းများကို ပုဒ်ဖြတ်ပုဒ်ရပ် ကော်မာ ထည့်ပေးခြင်း ဖြစ်ပါသည်
SELECT 
    department,
    COUNT(*) AS headcount,
    PRINTF('%,d MMK', SUM(base_salary)) AS total_payroll_cost,
    PRINTF('%,d MMK', CAST(AVG(base_salary) AS INT)) AS avg_salary
FROM employees
WHERE employment_status = 'Active'
GROUP BY department
ORDER BY SUM(base_salary) DESC;

-- 🔹 ဥပမာ (၃) - ကျား/မ (Gender) အလိုက် ပျမ်းမျှလစာ ကွာဟချက် စိစစ်ခြင်း (Gender Pay Equity)
SELECT 
    gender,
    COUNT(*) AS total_employees,
    PRINTF('%,d MMK', CAST(AVG(base_salary) AS INT)) AS avg_salary
FROM employees
WHERE employment_status = 'Active'
GROUP BY gender;
