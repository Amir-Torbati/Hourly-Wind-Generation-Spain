import requests
import pandas as pd
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import os

# --- Config ---
API_TOKEN = "478a759c0ef1ce824a835ddd699195ff0f66a9b5ae3b477e88a579c6b7ec47c5"
BASE_URL = "https://api.esios.ree.es/indicators/540"  # 🟢 Wind generation
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": API_TOKEN,
}

# --- Time: Spain local → UTC range (midnight to now) ---
now_local = datetime.now(ZoneInfo("Europe/Madrid")).replace(second=0, microsecond=0)
start_local = now_local.replace(hour=0, minute=0)

now_utc = start_local.astimezone(timezone.utc)
end_utc = now_local.astimezone(timezone.utc)

today_str = start_local.strftime("%Y-%m-%d")
daily_file = f"data/{today_str}-hourly.csv"
os.makedirs("data", exist_ok=True)

print(f"📡 Fetching hourly wind data from {start_local} to {now_local} (local time)")
print(f"📁 Saving to: {daily_file}")

# --- Load existing data if file exists ---
df_existing = pd.DataFrame()
if os.path.exists(daily_file):
    df_existing = pd.read_csv(daily_file, parse_dates=["datetime"])
    print(f"📄 Loaded existing file with {len(df_existing)} rows")

# --- Make API request ---
params = {
    "start_date": now_utc.isoformat(),
    "end_date": end_utc.isoformat(),
    "time_trunc": "hour"
}

try:
    res = requests.get(BASE_URL, headers=HEADERS, params=params)
    res.raise_for_status()
    data = res.json()["indicator"]["values"]
    print(f"📦 Received {len(data)} new rows from REE API")
except Exception as e:
    print(f"❌ API request failed: {e}")
    exit(1)

# --- Create DataFrame and process ---
df_new = pd.DataFrame(data)
if df_new.empty:
    print("⚠️ No new data returned — exiting.")
    exit(0)

df_new["datetime"] = pd.to_datetime(df_new["datetime"])
df_new = df_new.sort_values("datetime")

# --- Merge with existing and remove duplicates ---
df_combined = pd.concat([df_existing, df_new])
df_combined = df_combined.drop_duplicates(subset=["datetime"]).sort_values("datetime")

# --- Save result ---
df_combined.to_csv(daily_file, index=False)
print(f"✅ Synced {len(df_combined)} total rows to: {daily_file}")
print(f"📥 File exists: {os.path.exists(daily_file)}")
