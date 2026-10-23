# 📊 Enterprise Workforce & Payroll Intelligence Platform
> **End-to-End People Analytics & Business Intelligence Portfolio**  
> *Target Role: Data Analyst / People (HR) Analytics Specialist | Experience: 4+ Years HR Payroll Expertise*

---

## 📌 1. Executive Summary & Business Context

In a modern enterprise with **500 employees** and an annual payroll budget exceeding **10 Billion MMK (~10,251,842,998 MMK)**, leadership lacked centralized, automated visibility into workforce dynamics, compensation structures, and payroll leakage risks.

This project delivers a production-grade **People Analytics & Payroll Intelligence System** integrating **Relational SQL Database Architecture, Automated Python ETL Pipelines, and an Executive Dark-Mode Power BI Dashboard** (benchmarked against international banking dashboards).

---

## 🏗️ 2. End-to-End System Architecture

```mermaid
flowchart LR
    subgraph Layer1["1. Database & Storage Layer"]
        DB[(hr_payroll.db<br/>SQLite Relational DB)]
        T1[employees - 500 records]
        T2[payroll_records - 5,097 txns]
        T3[attendance_records - 5,097 txns]
        DB --- T1
        DB --- T2
        DB --- T3
    end

    subgraph Layer2["2. Automation & ETL Engine"]
        PY[Python Engine - Pandas]
        ETL[Star Schema Generator<br/>prepare_powerbi_data.py]
        AUDIT[SQL Audit Scripts<br/>day03_advanced_analytics.sql]
        PY --> ETL
        PY --> AUDIT
    end

    subgraph Layer3["3. Data Warehouse / Star Schema"]
        DIM[Dim_Employees<br/>Demographics, Status, Department]
        FACT[Fact_Payroll_History<br/>Monthly Pay, OT, Deductions]
        ETL --> DIM
        ETL --> FACT
    end

    subgraph Layer4["4. Executive Intelligence"]
        PBI[Power BI Desktop<br/>HR Dashboard.pbix]
        KPI[Top KPI Cards<br/>10bn Payroll | 406 Headcount | 18.8% Attrition]
        VIZ[Interactive Charts<br/>12-Mo Trend | Gender Donut | Dept Bar | Matrix]
        DIM --> PBI
        FACT --> PBI
        PBI --> KPI
        PBI --> VIZ
    end

    Layer1 -->|Direct Query & JOINs| Layer2
```

---

## 💡 3. Key Business Insights Discovered

### 🔍 1. Attrition Rate & Turnover Hotspots
* **Enterprise Attrition:** Company-wide attrition stands at **18.8%** (94 resigned out of 500 total workforce).
* **Department Hotspot:** **HR Department has the highest attrition rate at 22.1%**, followed by **Engineering at 19.3%**.
* **Strategic Recommendation:** Conduct retention interviews and compensation benchmarking for Tech and HR teams to curb high-cost turnover.

### 💰 2. Payroll Cost vs. Headcount Disparity
* **Engineering:** Accounts for **17.5% of active headcount (71/406)** but consumes **25.1% of total gross payroll (2.57 Billion MMK)** with Tech Leads earning up to 5,003,078 MMK/month.
* **Operations:** Accounts for **15.5% of active headcount (63/406)** but consumes only **12.2% of payroll (1.25 Billion MMK)**.

### 📈 3. Payroll Seasonality & Month-over-Month (MoM) Growth
* **February 2026 Peak:** Gross payroll surged to **888,144,506 MMK (+4.2% MoM growth)** due to annual bonus distributions and performance salary adjustments.
* **Q3 Downward Trend:** Payroll gradually contracted to **829,086,184 MMK by September (-1.05% MoM)** reflecting un-backfilled vacancies caused by the 18.8% cumulative attrition.

### ⚠️ 4. Overtime Outliers & Compliance Risk
* Specific Operations Supervisors and Sales Executives clocked **80 to 92.9 Overtime Hours in a single month**.
* Overtime Pay accounted for **over 40% to 43.3% of their total gross salary**, exposing operational burnout and headcount shortage risks.

---

## 🧮 4. Advanced DAX Measures (Power BI)

### 1. Active Headcount
```dax
Active Headcount = 
CALCULATE(
    COUNTROWS('Dim_Employees'),
    'Dim_Employees'[employment_status] = "Active"
)
```

### 2. Enterprise Attrition Rate
```dax
Attrition Rate = 
DIVIDE(
    CALCULATE(
        COUNTROWS('Dim_Employees'),
        'Dim_Employees'[employment_status] = "Resigned"
    ),
    COUNTROWS('Dim_Employees'),
    0
)
```

---

## ⚡ 5. Advanced SQL Analytics Showcase (Day 3)

### 1. Window Function: Top 2 Earners per Department
```sql
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
```

### 2. LAG() Window Function: Month-over-Month Payroll Growth
```sql
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
    ROUND((total_gross - LAG(total_gross) OVER (ORDER BY payroll_month)) * 100.0 / LAG(total_gross) OVER (ORDER BY payroll_month), 2) || '%' AS mom_growth_pct
FROM MonthlyPayroll;
```

---

## 🚀 6. How to Reproduce & Run Locally

### Prerequisites
* Python 3.10+
* Power BI Desktop (Windows)

### Step 1: Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-username/workforce-payroll-intelligence.git
cd workforce-payroll-intelligence
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run Advanced SQL Analytics
```bash
python 01_sql_analytics/run_query.py 01_sql_analytics/day03_advanced_analytics.sql
```

### Step 3: Open Power BI Dashboard
Open `03_powerbi_dashboards/HR Dashboard.pbix` in Power BI Desktop to explore the interactive visual analytics.

---

## 👤 Author & Candidate Profile
* **Domain Expertise:** HR Management, Payroll Administration, Tax & SSB Compliance (4 Years Senior Executive Experience)
* **Technical Skills:** SQL (Advanced Window Functions, CTEs, Joins), Python (Pandas, NumPy, SQLite3, Automation), Power BI (Star Schema Modeling, DAX, Dark Mode Dashboard Design)
* **Career Objective:** Transitioning into **Senior Data Analyst / People Analytics Specialist** role.
