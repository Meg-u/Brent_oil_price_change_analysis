# Brent Oil Change Point Analysis

## Overview

This repository investigates structural changes in Brent oil prices in response to geopolitical and economic events using Bayesian change point detection (PyMC3).

## Task 1: Problem Definition & Event Data Curation

### Objectives:

- Define the project scope and methodology
- Curate impactful events likely to cause changes in oil price
- Document time series properties and workflow

### Files:

- `data/brent_oil_events.csv`: Event metadata aligned with historical context
- `reports/Task1_Report_Brent_Oil_Analysis.pdf`: Summary of Task 1

### Workflow Reference:

- Data Science PM Framework
- Bayesian change point detection guides

Tasks Completed
Task 2 – Data Preparation & EDA
Collected Brent oil price historical dataset (BrentOilPrices.csv)

Cleaned and formatted date columns

Plotted:

Raw price trend over time

Log returns for volatility analysis

Saved cleaned dataset: data/brent_oil_cleaned.csv

– Change Point Modeling & Insight Generation
Implemented a Bayesian Change Point model in PyMC to detect structural breaks in the price series.

Identified most probable change point date (April 2004 in this run).

Quantified the impact:

Mean price before vs after change point

Volatility before vs after change point

% change in mean price

Associated change points with potential geopolitical events from research (e.g., US-led invasion of Iraq).

Saved results to outputs/change_point_impact.csv

Advanced Extension: Future work could include macroeconomic indicators (GDP, USD index, etc.) to explain price shifts.

Task 3 – Interactive Dashboard
Backend (Flask):

APIs to serve change point results and historical price data

Data fetched from CSV outputs of Task 2

Frontend (React):

Table showing change point impact summary

Line chart of Brent oil price over time

Interactive & responsive design

Tech stack: Flask (Python), React (JavaScript), Recharts, Axios

How to Run
#Backend (Flask)
cd backend
pip install -r requirements.txt
python app.py
#Frontend (React)
cd frontend
npm install
npm start
Outputs
Change Point Impact Summary Table

Historical Brent Oil Price Chart

Data accessible via API:

GET /api/impact

GET /api/prices
