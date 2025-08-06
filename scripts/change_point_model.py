# scripts/change_point_model.py

import pymc as pm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
def load_data():
    df = pd.read_csv("data/brent_oil_cleaned.csv", parse_dates=["Date"])
    df["log_price"] = np.log(df["Price"])
    return df

def build_model(data):
    n = len(data)
    with pm.Model() as model:
        tau = pm.DiscreteUniform("tau", lower=0, upper=n - 1)
        mu1 = pm.Normal("mu1", mu=0, sigma=10)
        mu2 = pm.Normal("mu2", mu=0, sigma=10)
        sigma1 = pm.HalfNormal("sigma1", sigma=10)
        sigma2 = pm.HalfNormal("sigma2", sigma=10)

        mu = pm.math.switch(tau >= np.arange(n), mu1, mu2)
        sigma = pm.math.switch(tau >= np.arange(n), sigma1, sigma2)

        pm.Normal("obs", mu=mu, sigma=sigma, observed=data)
    return model

def run_inference(model):
    with model:
        trace = pm.sample(2000, tune=1000, return_inferencedata=True, target_accept=0.95)
    return trace

def plot_results(trace, data, dates):
    tau_samples = trace.posterior["tau"].values.flatten()
    tau_mean = int(np.mean(tau_samples))

    plt.figure(figsize=(12, 6))
    plt.plot(dates, data, label="Log Price")
    plt.axvline(dates[tau_mean], color="red", linestyle="--", 
                label=f"Estimated Change Point: {dates[tau_mean].date()}")
    plt.title("Bayesian Change Point Detection")
    plt.xlabel("Date")
    plt.ylabel("Log(Price)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    return tau_mean

if __name__ == "__main__":
    # Step 1: Load data
    df = load_data()

    # Step 2: Build and run model
    model = build_model(df["log_price"].values)
    trace = run_inference(model)

    # Step 3: Plot and get change point index
    tau_estimated_index = plot_results(trace, df["log_price"].values, df["Date"])
    change_point_date = df['Date'].iloc[tau_estimated_index]

    # Step 4: Quantify impact
    before_df = df[df['Date'] < change_point_date]
    after_df = df[df['Date'] >= change_point_date]

    # Mean log price
    mean_log_before = before_df['log_price'].mean()
    mean_log_after = after_df['log_price'].mean()

    # Mean actual price
    mean_price_before = before_df['Price'].mean()
    mean_price_after = after_df['Price'].mean()

    # Std deviation (volatility)
    vol_before = before_df['Price'].std()
    vol_after = after_df['Price'].std()

    # Percentage change in mean price
    pct_change_mean = ((mean_price_after - mean_price_before) / mean_price_before) * 100

    # Save results
    impact_summary = {
        "Change Point Date": change_point_date.strftime("%Y-%m-%d"),
        "Mean Price Before": mean_price_before,
        "Mean Price After": mean_price_after,
        "Percent Change in Mean Price": pct_change_mean,
        "Volatility Before": vol_before,
        "Volatility After": vol_after
    }

    os.makedirs("outputs", exist_ok=True)
    impact_df = pd.DataFrame([impact_summary])
    impact_df.to_csv("outputs/change_point_impact.csv", index=False)

    print("\n--- Change Point Impact Summary ---")
    print(impact_df.to_string(index=False))

    # --- Cause Association Step ---
    # Closest researched event from Task 1
    event_date = pd.to_datetime("2003-03-20")
    event_desc = "US-led invasion of Iraq begins"
    event_type = "Geopolitical"

# Calculate gap between detected change point and researched event
    days_diff = (change_point_date - event_date).days

# Interpretation text
    interpretation = f"""
    --- Cause Association ---
    Detected change point: {change_point_date.strftime('%Y-%m-%d')}
    Closest researched event: {event_date.strftime('%Y-%m-%d')} - {event_desc} ({event_type})
    Time difference: {days_diff} days (~{days_diff/30:.1f} months)

    Interpretation:
    The detected structural break occurred about {days_diff/30:.1f} months after the invasion of Iraq.
    While the invasion itself introduced geopolitical risk, the sustained instability through 2003–2004
    likely amplified oil supply concerns, driving the transition to a higher price regime.
    During this shift, the mean Brent oil price rose from ${mean_price_before:.2f} to ${mean_price_after:.2f}
    (a {pct_change_mean:.1f}% increase), and volatility increased from {vol_before:.2f} to {vol_after:.2f}.
    This suggests that the market's reaction was not instantaneous but developed over time as
    supply disruptions and demand pressures accumulated.
    """
    print(interpretation)

# Save to text file for reporting
    with open("outputs/cause_association.txt", "w") as f:
        f.write(interpretation)
