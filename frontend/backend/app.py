# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allow requests from React

# Helper function to get file path relative to backend/
def rel_path(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *parts))

# Load change point impact results
impact_file = rel_path("..","outputs", "change_point_impact.csv")
if os.path.exists(impact_file):
    impact_df = pd.read_csv(impact_file)

    # Ensure consistent column names for React table
    expected_cols = [
        "Change Point Date",
        "Mean Price Before",
        "Mean Price After",
        "Percent Change in Mean Price",
        "Volatility Before",
        "Volatility After"
    ]
    if list(impact_df.columns) != expected_cols:
        impact_df.columns = expected_cols
else:
    impact_df = pd.DataFrame()

# Load cleaned Brent oil price data
price_file = rel_path("..","data", "brent_oil_cleaned.csv")
if os.path.exists(price_file):
    price_df = pd.read_csv(price_file, parse_dates=["Date"])
else:
    price_df = pd.DataFrame()

@app.route("/api/impact", methods=["GET"])
def get_impact():
    """Return change point impact summary."""
    return jsonify(impact_df.to_dict(orient="records"))

@app.route("/api/prices", methods=["GET"])
def get_prices():
    """Return historical price data."""
    if price_df.empty:
        return jsonify([])

    df = price_df.copy()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")  # Convert datetime to string for JSON
    return jsonify(df[["Date", "Price"]].to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/")
def home():
    return "Flask API is running. Use /api/impact or /api/prices."