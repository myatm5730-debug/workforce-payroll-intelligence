# ==============================================================================
# 🔰 အဆင့် (၂): Python ဖြင့် CSV ဖိုင်ကို ဖတ်ယူခြင်း (READING CSV WITH PANDAS)
# ==============================================================================

# ၁။ Pandas Library ကို စတင်ခေါ်ယူခြင်း
import pandas as pd

# ၂။ CSV ဖိုင်ကို ဖွင့်ပြီး df (DataFrame) ဇယားထဲ ထည့်ခြင်း
df = pd.read_csv("data/employees.csv")

print("=" * 70)
print("✅ ၁။ ဒေတာဖိုင် အောင်မြင်စွာ ဖတ်ယူပြီးပါပြီ!")
print("=" * 70)

# ၃။ ဇယား အရွယ်အစား (Row ဘယ်နှစ်ခု၊ Column ဘယ်နှစ်ခု ရှိသလဲ စစ်ဆေးခြင်း)
# df.shape -> (Rows, Columns)
rows, cols = df.shape
print(f"📊 ဝန်ထမ်းဦးရေ (Rows): {rows} ဦး")
print(f"📊 အချက်အလက်ကော်လံ (Columns): {cols} ခု\n")

# ၄။ ပထမဆုံး ဝန်ထမ်း ၅ ယောက်၏ အချက်အလက်ကို ပြသခြင်း (df.head())
print("📋 ပထမဆုံး ဝန်ထမ်း ၅ ဦး၏ Data:")
print(df[['emp_id', 'name', 'department', 'job_title', 'base_salary']].head())

print("\n" + "=" * 70)
# ၅။ အခြေခံလစာ စာရင်းအနှစ်ချုပ် (ပျမ်းမျှလစာ၊ အနည်းဆုံး၊ အများဆုံး)
avg_salary = df['base_salary'].mean()
min_salary = df['base_salary'].min()
max_salary = df['base_salary'].max()

print(f"💰 ပျမ်းမျှလစာ (Average): {int(avg_salary):,} MMK")
print(f"💰 အနိမ့်ဆုံးလစာ (Minimum): {int(min_salary):,} MMK")
print(f"💰 အမြင့်ဆုံးလစာ (Maximum): {int(max_salary):,} MMK")
print("=" * 70)
