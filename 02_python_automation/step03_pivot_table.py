# ==============================================================================
# 🔰 အဆင့် (၃): Python ဖြင့် Excel Pivot Table ဆွဲခြင်း (PIVOT TABLE IN PYTHON)
# ==============================================================================

import pandas as pd

# ၁။ Data ဖိုင်ကို ဖတ်ယူခြင်း
df = pd.read_csv("data/employees.csv")

# Active ဝန်ထမ်းများကိုသာ စိစစ်ခြင်း
df_active = df[df['employment_status'] == 'Active']

print("=" * 80)
print("📊 PIVOT TABLE (၁): ဌာနအလိုက် ပျမ်းမျှလစာနှင့် ဝန်ထမ်းဦးရေ")
print("=" * 80)

# Excel မှာ Rows ထဲကို Department ထည့်ပြီး Values ထဲကို Salary ထည့်သလိုမျိုး:
pivot1 = df_active.pivot_table(
    index='department',           # Excel ရဲ့ 'Rows'
    values='base_salary',         # Excel ရဲ့ 'Values'
    aggfunc=['count', 'mean']     # Excel ရဲ့ 'Count' နှင့် 'Average'
)

# Column နာမည်များကို ရှင်းလင်းအောင် ပြင်ဆင်ခြင်း
pivot1.columns = ['Headcount (ဦးရေ)', 'Avg Salary (ပျမ်းမျှလစာ)']
pivot1['Avg Salary (ပျမ်းမျှလစာ)'] = pivot1['Avg Salary (ပျမ်းမျှလစာ)'].map('{:,.0f} MMK'.format)
print(pivot1)


print("\n" + "=" * 80)
print("📊 PIVOT TABLE (၂): ဌာနအလိုက် ကျား/မ ပျမ်းမျှလစာ ကွာဟချက် (CROSS-TABULATION)")
print("=" * 80)

# Excel မှာ Rows ထဲကို Department ထည့်၊ Columns ထဲကို Gender ထည့်သလိုမျိုး:
pivot2 = df_active.pivot_table(
    index='department',           # Excel ရဲ့ 'Rows'
    columns='gender',             # Excel ရဲ့ 'Columns'
    values='base_salary',         # Excel ရဲ့ 'Values'
    aggfunc='mean'                # Excel ရဲ့ 'Average'
)

# Format to MMK
pivot2_formatted = pivot2.map(lambda x: f"{int(x):,} MMK" if pd.notnull(x) else "-")
print(pivot2_formatted)


print("\n" + "=" * 80)
print("📊 PIVOT TABLE (၃): ပညာအရည်အချင်းအလိုက် ဝန်ထမ်းဦးရေနှင့် အမြင့်ဆုံး/အနိမ့်ဆုံး လစာ")
print("=" * 80)

pivot3 = df_active.pivot_table(
    index='education',
    values='base_salary',
    aggfunc=['count', 'min', 'max']
)
pivot3.columns = ['ဦးရေ', 'အနိမ့်ဆုံးလစာ', 'အမြင့်ဆုံးလစာ']
pivot3['အနိမ့်ဆုံးလစာ'] = pivot3['အနိမ့်ဆုံးလစာ'].map('{:,.0f} MMK'.format)
pivot3['အမြင့်ဆုံးလစာ'] = pivot3['အမြင့်ဆုံးလစာ'].map('{:,.0f} MMK'.format)
print(pivot3)
print("=" * 80)
