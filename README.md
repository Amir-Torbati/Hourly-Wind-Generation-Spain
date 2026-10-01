## Collection migration - 1 October 2026

Active collection has moved to the grouped five-curve workflow in [Energy Data Collection](https://github.com/Amir-Torbati/ree-data-platform/blob/main/docs/FUNDAMENTALS.md) (owner access required). It collects verified ESIOS indicators 1295 (actual PV), 551 (actual wind), 1293 (actual demand), 542 (PV forecast) and 541 (wind forecast).

**The files below are a preserved legacy archive, not certified actual-generation data.** The review found source-ID mismatches in the solar/wind collectors and reliability problems in the demand scraper. Current code alone does not establish the origin of every historical file. Do not combine this archive with the corrected curves without checking provenance. Legacy collection/backfill workflows are retired to prevent overlapping or mislabelled downloads. Data files and Git history have not been deleted or relabelled.

---

🌬️ Hourly Wind Generation – Spain (Hourly Resolution)
This project collects and stores real-time hourly wind power generation data for the Peninsular region of Spain, using the official Red Eléctrica de España (ESIOS) API.

We built a fully automated data pipeline that updates every hour and stores results in structured daily files — ready for analysis, modeling, forecasting, or integration into energy dashboards.

📁 Folder Structure

data/
└── YYYY-MM-DD-hourly.csv     ← Hourly wind data for each day

scripts/
└── collect_wind_hourly.py    ← Python script to fetch wind data

.github/workflows/
└── fetch_wind_data.yml       ← GitHub Actions workflow (runs hourly)

🔄 What’s Automated?
✅ Real-Time Fetching (fetch_wind_data.yml)

      - Pulls hourly wind generation data from the ESIOS API
      - Runs every hour via GitHub Actions
      - Saves new data to data/YYYY-MM-DD-hourly.csv
      - Automatically appends and deduplicates safely

✅ Timezone-Aware Storage

      - Uses Spain local calendar (Europe/Madrid)
      - Converts timestamps to UTC for consistency
      - Files are named using the local Spain date (e.g. 2025-04-14-hourly.csv)

🧠 Scripts
collect_wind_hourly.py

     - Converts local Spain time to UTC
     - Uses time_trunc = "hour" for hourly resolution
     - Loads today's file if it exists
     - Appends new hourly rows
     - Deduplicates by timestamp (datetime column)
     - Writes clean output back to the CSV

🛠 Tech Stack
     - Python 3.11
     - Pandas
     - Requests
     - GitHub Actions

Red Eléctrica de España (ESIOS API)

📡 Data Source
    - Provider: Red Eléctrica de España (REE)
    - API: https://api.esios.ree.es/
    - Indicator: 540 (Wind Generation - Peninsular)
    - Timezone: Timestamps in UTC, filenames by Spain local date

🗺️ Roadmap
✅ Collect hourly wind generation
✅ Store daily files in data/ folder
✅ GitHub Actions automation
🔜 Add .parquet + DuckDB versions
🔜 Backfill historical data from 2023
🔜 Live dashboard with Streamlit or Looker
🔜 Merge with weather + OMIE price data
🔜 BESS optimization using wind data

👤 Author
Created with 💨 by Amir Torbati
All rights reserved © 2025

Please cite or credit if you use this project in academic, research, or commercial settings.

⚡ Let the wind power your models.
