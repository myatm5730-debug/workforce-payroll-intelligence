-- ==============================================================================
-- 🎯 DAY 3: ADVANCED SQL FOR DATA ANALYSTS (INTERVIEW GOLD STANDARD)
-- Focus: Window Functions (ROW_NUMBER, PARTITION BY, LAG), CTEs, Business Audits
-- Database: data/hr_payroll.db
-- Runner: python 01_sql_analytics/run_query.py 01_sql_analytics/day03_advanced_analytics.sql
-- ==============================================================================

-- 🔹 မေးခွန်း (၁) - ဌာနတစ်ခုချင်းစီအလိုက် လစာအမြင့်ဆုံး ထိပ်တန်း (၂) ယောက်စီကို ရှာဖွေခြင်း
-- Key Technique: CTE (WITH ... AS) + Window Function (ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...))
WITH RankedSalaries AS (
    SELECT 
        emp_id,
        name,
        department,
        job_title,
        base_salary,
        ROW_NUMBER() OVER (
            PARTITION BY department 
            ORDER BY base_salary DESC
        ) AS rank_in_dept
    FROM employees
    WHERE employment_status = 'Active'
)
SELECT 
    department,
    rank_in_dept,
    name,
    job_title,
    PRINTF('%,d MMK', base_salary) AS monthly_salary
FROM RankedSalaries
WHERE rank_in_dept <= 2
ORDER BY department, rank_in_dept;

-- 🔹 မေးခွန်း (၂) - လစဉ် Payroll ကုန်ကျစရိတ် ပြောင်းလဲမှု (Month-over-Month Growth %)
-- Key Technique: LAG() Window Function (ယခင်လ တန်ဖိုးကို ယူငင်ပြီး လက်ရှိလနှင့် နှိုင်းယှဉ်ခြင်း)
-- (Power BI Line Chart မှာ မြင်တွေ့ခဲ့ရတဲ့ Feb/March Peak နဲ့ September Dip ရဲ့ အဖြေဖြစ်ပါသည်)
WITH MonthlyPayroll AS (
    SELECT 
        STRFTIME('%Y-%m', payroll_date) AS payroll_month,
        SUM(gross_salary) AS total_gross
    FROM payroll_records
    GROUP BY STRFTIME('%Y-%m', payroll_date)
)
SELECT 
    payroll_month,
    PRINTF('%,d MMK', total_gross) AS current_month_gross,
    PRINTF('%,d MMK', COALESCE(LAG(total_gross) OVER (ORDER BY payroll_month), 0)) AS prev_month_gross,
    CASE 
        WHEN LAG(total_gross) OVER (ORDER BY payroll_month) IS NULL THEN 'Baseline'
        ELSE ROUND((total_gross - LAG(total_gross) OVER (ORDER BY payroll_month)) * 100.0 / LAG(total_gross) OVER (ORDER BY payroll_month), 2) || '%'
    END AS mom_growth_pct
FROM MonthlyPayroll;

-- 🔹 မေးခွန်း (၃) - အချိန်ပိုကြေး (Overtime) သုံးစွဲမှု မူမမှန်သူများကို စိစစ်ဖော်ထုတ်ခြင်း (Audit Analysis)
-- Key Technique: Multi-table JOIN + Conditional Filtering (OT Pay သည် Gross Salary ရဲ့ 35% ကျော်နေသူများ)
SELECT 
    e.name,
    e.department,
    e.job_title,
    p.payroll_date,
    p.ot_hours,
    PRINTF('%,d MMK', p.ot_pay) AS ot_pay,
    PRINTF('%,d MMK', p.gross_salary) AS gross_salary,
    ROUND(p.ot_pay * 100.0 / p.gross_salary, 1) || '%' AS ot_percentage
FROM payroll_records p
JOIN employees e ON p.emp_id = e.emp_id
WHERE p.ot_hours >= 35 
  AND (p.ot_pay * 1.0 / p.gross_salary) >= 0.35
ORDER BY p.ot_hours DESC
LIMIT 8;
