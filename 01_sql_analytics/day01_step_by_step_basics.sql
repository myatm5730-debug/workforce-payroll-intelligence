-- ==============================================================================
-- 🔰 DAY 1: SQL STEP-BY-STEP BASICS (EXCEL အခြေခံနှင့် နှိုင်းယှဉ်လေ့လာခြင်း)
-- Database: data/hr_payroll.db
-- ==============================================================================

-- 🔹 အဆင့် (၁) - Excel Sheet တစ်ခုလုံးကို ဖွင့်ကြည့်သလို အားလုံးကြည့်ခြင်း (LIMIT 5 = ပထမ ၅ ယောက်)
-- သင်္ကေတ (*) ဆိုသည်မှာ "Column အကုန်လုံးကို ပြပါ" ဟု အဓိပ္ပာယ်ရပါသည်။
SELECT * 
FROM employees 
LIMIT 5;

-- 🔹 အဆင့် (၂) - ကိုယ်လိုချင်သော Column သီးသန့် ၃ ခုကိုသာ ရွေးကြည့်ခြင်း
SELECT 
    emp_id, 
    name, 
    job_title, 
    base_salary 
FROM employees 
LIMIT 5;

-- 🔹 အဆင့် (၃) - Excel Filter ကဲ့သို့ အခြေအနေတစ်ခု သတ်မှတ် စစ်ထုတ်ခြင်း (WHERE)
-- "HR ဌာနမှ ဝန်ထမ်းများကိုသာ ပြပါ"
SELECT 
    name, 
    department, 
    job_title, 
    base_salary 
FROM employees 
WHERE department = 'HR'
LIMIT 5;

-- 🔹 အဆင့် (၄) - စည်းကမ်းချက် ၂ ခု ပေါင်းစပ် စစ်ထုတ်ခြင်း (AND)
-- "HR ဌာန ဖြစ်ပြီး လစာ ၁၀ သိန်းအောက် (1,000,000) ရရှိသူများ"
SELECT 
    name, 
    department, 
    job_title, 
    base_salary 
FROM employees 
WHERE department = 'HR' 
  AND base_salary < 1000000;

-- 🔹 အဆင့် (၅) - Excel တွင် =COUNT(...) သုံးသကဲ့သို့ အရေအတွက် ရေတွက်ခြင်း
-- "၂၀၂၃ နောက်ပိုင်း ဝင်ပြီး လစာ ၁၀ သိန်းအောက် ရရှိသော Active ဝန်ထမ်း ဦးရေ"
SELECT 
    COUNT(*) AS total_employees
FROM employees 
WHERE hire_date >= '2023-01-01'
  AND base_salary < 1000000
  AND employment_status = 'Active';
