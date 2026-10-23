import sqlite3
import pandas as pd
import sys
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DB_PATH = "data/hr_payroll.db"

def run_script(sql_content):
    conn = sqlite3.connect(DB_PATH)
    try:
        # Split by semicolon, filter out empty queries
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for idx, stmt in enumerate(statements, 1):
            # Extract comment headers if any
            lines = stmt.splitlines()
            headers = [l for l in lines if l.strip().startswith('--')]
            query_lines = [l for l in lines if not l.strip().startswith('--')]
            query = "\n".join(query_lines).strip()
            
            if not query:
                continue
                
            print("\n" + "="*85)
            if headers:
                print("\n".join(headers))
                print("-" * 85)
            else:
                print(f"Query #{idx}:")
                
            df = pd.read_sql_query(query, conn)
            print(df)
            print(f"📊 Result: {len(df)} rows returned.")
            print("="*85)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query_file = sys.argv[1]
        with open(query_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📁 Running SQL Script: {query_file}")
        run_script(content)
    else:
        test_query = """
        -- Department Headcount Summary
        SELECT 
            department,
            COUNT(*) AS total_employees,
            PRINTF('%,d MMK', CAST(AVG(base_salary) AS INT)) AS avg_salary
        FROM employees
        WHERE employment_status = 'Active'
        GROUP BY department
        ORDER BY AVG(base_salary) DESC;
        """
        run_script(test_query)
