# scripts/generate_event_csv.py

import csv
import os

# Output path
output_dir = os.path.join("data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "brent_oil_events.csv")

# Manually curated major events affecting Brent oil prices
events = [
    {"Date": "1990-08-02", "Event_Description": "Iraq invades Kuwait, triggering Gulf War", "Event_Type": "Geopolitical"},
    {"Date": "2001-09-11", "Event_Description": "9/11 attacks in US, causing oil price volatility", "Event_Type": "Economic/Political"},
    {"Date": "2003-03-20", "Event_Description": "US-led invasion of Iraq begins", "Event_Type": "Geopolitical"},
    {"Date": "2008-09-15", "Event_Description": "Lehman Brothers collapses, global financial crisis", "Event_Type": "Economic"},
    {"Date": "2010-01-01", "Event_Description": "Arab Spring unrest begins in MENA region", "Event_Type": "Geopolitical"},
    {"Date": "2014-11-27", "Event_Description": "OPEC decides not to cut production amid price fall", "Event_Type": "OPEC Decision"},
    {"Date": "2016-11-30", "Event_Description": "OPEC agrees to production cut with Russia", "Event_Type": "OPEC Decision"},
    {"Date": "2019-09-14", "Event_Description": "Drone attacks on Saudi Aramco facilities", "Event_Type": "Geopolitical"},
    {"Date": "2020-03-08", "Event_Description": "Oil price war begins between Saudi and Russia", "Event_Type": "Economic/OPEC"},
    {"Date": "2020-04-20", "Event_Description": "US oil futures turn negative, Brent drops", "Event_Type": "Economic"},
    {"Date": "2022-02-24", "Event_Description": "Russia invades Ukraine", "Event_Type": "Geopolitical"},
    {"Date": "2022-10-05", "Event_Description": "OPEC+ announces deep production cuts", "Event_Type": "OPEC Decision"},
]

# Write CSV
with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Date", "Event_Description", "Event_Type"])
    writer.writeheader()
    for event in events:
        writer.writerow(event)

print(f"CSV written to: {output_path}")
