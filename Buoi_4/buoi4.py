# forecast_suite.py
# -*- coding: utf-8 -*-
"""
Full pipeline for the assignment:
- Q1: Trend regression for Sanluong
- Q2: Exponential smoothing (best of SES/Holt/HW) for Sanluong; and for Hoahong & CPQC
- Q3: Multiple regression with CPQC + Hoahong + seasonal dummies; forecast using ETS forecasts of CPQC & Hoahong
- Q4: Compare Model (2) vs Model (3) via holdout MAPE and recommend

USAGE (terminal):
    pip install pandas numpy matplotlib scikit-learn statsmodels pyreadstat
    python forecast_suite.py --sav "Du bao bang mo hinh nhan qua san luong _ CPQC Hoahong quy.sav" --h 4

Outputs:
- PNG charts for Q1, Q2a, Q2b (each regressor), Q3
- TXT summaries for regressions
- CSV forecasts for Q2a (Sanluong) and Q3
- metrics_summary.csv (MAPE, Adj_R2, AIC)
"""
import os
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing

def safe_mape(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = y_true != 0
    if mask.sum() == 0:
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask]))

def detect_column(df, candidates, required=False):
    lower_map = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    if required:
        raise KeyError(f"Missing required column; tried: {candidates}")
    return None

def ensure_trend_and_quarter(df):
    t_col = detect_column(df, ["t", "trend", "time_index"], required=False)
    if t_col is None:
        df = df.copy()
        df["t"] = np.arange(1, len(df) + 1)
        t_col = "t"
    q_col = detect_column(df, ["quarter", "quy", "q", "Quarter", "Quy"], required=False)
    if q_col is None:
        df = df.copy()
        df["quarter"] = ((df[t_col].astype(int) - 1) % 4) + 1
        q_col = "quarter"
    for q in [2,3,4]:
        df[f"Q{q}"] = (df[q_col] == q).astype(int)
    return df, t_col, q_col

def fit_best_ets(y, seasonal_periods=4):
    results = {}
    y = pd.Series(y).astype(float)
    try:
        ses = SimpleExpSmoothing(y, initialization_method="heuristic").fit()
        results["SES"] = {"model": ses, "aic": getattr(ses, "aic", np.nan)}
    except Exception:
        results["SES"] = {"model": None, "aic": np.inf}
    try:
        holt = Holt(y, initialization_method="heuristic").fit()
        results["Holt"] = {"model": holt, "aic": getattr(holt, "aic", np.nan)}
    except Exception:
        results["Holt"] = {"model": None, "aic": np.inf}
    try:
        hw = ExponentialSmoothing(y, trend="add", seasonal="add", seasonal_periods=seasonal_periods,
                                  initialization_method="heuristic").fit(optimized=True)
        results["HW_add"] = {"model": hw, "aic": getattr(hw, "aic", np.nan)}
    except Exception:
        results["HW_add"] = {"model": None, "aic": np.inf}
    best_name, best_info = min(results.items(), key=lambda kv: kv[1]["aic"])
    return best_name, best_info["model"], results

def train_test_split_time(df, test_h=4):
    if len(df) <= test_h:
        return df.copy(), df.iloc[0:0].copy()
    return df.iloc[:-test_h].copy(), df.iloc[-test_h:].copy()

def save_fig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

def read_sav_any(sav_path):
    # Try pandas.read_spss (which needs pyreadstat) first, then pyreadstat directly
    try:
        df = pd.read_spss(sav_path)
        return df
    except Exception as e:
        try:
            import pyreadstat
            df, meta = pyreadstat.read_sav(sav_path)
            return df
        except Exception as e2:
            raise RuntimeError(
                f"Không thể đọc file .sav. Cài đặt 'pyreadstat' rồi thử lại.\n"
                f"Errors:\n- pandas.read_spss: {e}\n- pyreadstat: {e2}"
            )

def main(args):
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    df = read_sav_any(args.sav)
    df.columns = [c.strip() for c in df.columns]

    y_col = detect_column(df, ["Sanluong", "sanluong", "Output", "Y"], required=True)
    cpqc_col = detect_column(df, ["CPQC", "cpqc"], required=False)
    hh_col = detect_column(df, ["Hoahong", "hoahong", "HoaHong"], required=False)

    df, t_col, q_col = ensure_trend_and_quarter(df)

    model_df = df[[y_col, t_col]].copy()
    if cpqc_col is not None:
        model_df["CPQC"] = df[cpqc_col]
    if hh_col is not None:
        model_df["Hoahong"] = df[hh_col]
    for q in [2,3,4]:
        model_df[f"Q{q}"] = df[f"Q{q}"]

    # Create quarterly DateTimeIndex for plotting (display only)
    periods = len(model_df)
    idx = pd.period_range(start=pd.Period("2000Q1", freq="Q"), periods=periods).to_timestamp(how="end")
    model_df.index = idx

    # ---- Q1: Trend regression ----
    X1 = sm.add_constant(model_df[[t_col]])
    y = model_df[y_col].astype(float)
    ols1 = sm.OLS(y, X1).fit()
    model_df["yhat_q1"] = ols1.predict(X1)
    mape_q1 = safe_mape(y, model_df["yhat_q1"])

    plt.figure()
    plt.plot(model_df.index, y, label="Actual")
    plt.plot(model_df.index, model_df["yhat_q1"], label="Fitted (Trend)")
    plt.title("Q1: Trend Regression — Actual vs Fitted")
    plt.xlabel("Time")
    plt.ylabel(y_col)
    plt.legend()
    save_fig(os.path.join(outdir, "q1_trend_regression.png"))

    with open(os.path.join(outdir, "q1_ols_summary.txt"), "w", encoding="utf-8") as f:
        f.write(ols1.summary().as_text())

    # ---- Q2: ETS for Sanluong ----
    best_name_y, best_model_y, _ = fit_best_ets(model_df[y_col].values, seasonal_periods=4)
    fitted_y = best_model_y.fittedvalues if hasattr(best_model_y, "fittedvalues") else best_model_y.predict(start=0, end=len(model_df)-1)
    mape_q2_y = safe_mape(model_df[y_col].values, fitted_y)

    h = args.h
    fc_index = pd.period_range(model_df.index[-1].to_period("Q")+1, periods=h, freq="Q").to_timestamp(how="end")
    fc_y = best_model_y.forecast(h)
    q2_sanluong_forecast = pd.Series(fc_y, index=fc_index, name="Sanluong_forecast")
    q2_sanluong_forecast.to_csv(os.path.join(outdir, "q2a_sanluong_forecast.csv"), index_label="date")

    plt.figure()
    plt.plot(model_df.index, model_df[y_col], label="Actual")
    plt.plot(model_df.index, fitted_y, label=f"Fitted ({best_name_y})")
    plt.plot(fc_index, q2_sanluong_forecast.values, label="Forecast (next {})".format(h))
    plt.title(f"Q2a: Exponential Smoothing for {y_col}")
    plt.xlabel("Time")
    plt.ylabel(y_col)
    plt.legend()
    save_fig(os.path.join(outdir, "q2a_ets_sanluong.png"))

    # Q2b: ETS for regressors
    ets_regressors = {}
    for col in ["Hoahong", "CPQC"]:
        if col in model_df.columns:
            best_name, best_model, _ = fit_best_ets(model_df[col].astype(float).values, seasonal_periods=4)
            fitted = best_model.fittedvalues if hasattr(best_model, "fittedvalues") else best_model.predict(start=0, end=len(model_df)-1)
            mape = safe_mape(model_df[col].values, fitted)
            fc = best_model.forecast(h)
            ets_regressors[col] = {"best": best_name, "model": best_model, "fitted": fitted, "mape": mape, "forecast": fc}

            plt.figure()
            plt.plot(model_df.index, model_df[col].values, label="Actual")
            plt.plot(model_df.index, fitted, label=f"Fitted ({best_name})")
            plt.plot(fc_index, fc, label="Forecast (next {})".format(h))
            plt.title(f"Q2b: Exponential Smoothing for {col}")
            plt.xlabel("Time")
            plt.ylabel(col)
            plt.legend()
            save_fig(os.path.join(outdir, f"q2b_ets_{col.lower()}.png"))

    # ---- Q3: Multiple regression with seasonal dummies ----
    X_cols = [t_col, "CPQC", "Hoahong", "Q2", "Q3", "Q4"]
    X_cols = [c for c in X_cols if c in model_df.columns]
    X3 = sm.add_constant(model_df[X_cols])
    ols3 = sm.OLS(y, X3).fit()
    model_df["yhat_q3_insample"] = ols3.predict(X3)
    mape_q3_in = safe_mape(y, model_df["yhat_q3_insample"])

    # Build future design
    future_df = pd.DataFrame(index=fc_index)
    future_df[t_col] = np.arange(model_df[t_col].iloc[-1] + 1, model_df[t_col].iloc[-1] + h + 1)
    future_quarters = (((future_df[t_col].astype(int) - 1) % 4) + 1).values
    for q in [2,3,4]:
        future_df[f"Q{q}"] = (future_quarters == q).astype(int)
    if "CPQC" in X_cols and "CPQC" in ets_regressors:
        future_df["CPQC"] = ets_regressors["CPQC"]["forecast"]
    if "Hoahong" in X_cols and "Hoahong" in ets_regressors:
        future_df["Hoahong"] = ets_regressors["Hoahong"]["forecast"]

    X3_future = sm.add_constant(future_df[X_cols], has_constant="add")
    q3_forecast = ols3.predict(X3_future)
    q3_forecast = pd.Series(q3_forecast, index=fc_index, name="Sanluong_forecast_q3")
    q3_forecast.to_csv(os.path.join(outdir, "q3_sanluong_forecast.csv"), index_label="date")

    plt.figure()
    plt.plot(model_df.index, model_df[y_col], label="Actual")
    plt.plot(model_df.index, model_df["yhat_q3_insample"], label="Fitted (Q3 model)")
    plt.plot(fc_index, q3_forecast.values, label="Forecast (Q3 model)")
    plt.title("Q3: Multiple Regression Forecast (with ETS regressors)")
    plt.xlabel("Time")
    plt.ylabel(y_col)
    plt.legend()
    save_fig(os.path.join(outdir, "q3_multireg_forecast.png"))

    with open(os.path.join(outdir, "q3_ols_summary.txt"), "w", encoding="utf-8") as f:
        f.write(ols3.summary().as_text())

    # ---- Q4: Compare Model (2) vs (3) on holdout ----
    train_df, test_df = train_test_split_time(model_df, test_h=4)

    X_cols_2 = [t_col, "CPQC", "Hoahong", "Q2", "Q3", "Q4"]
    X_cols_2 = [c for c in X_cols_2 if c in train_df.columns]
    X_train_2 = sm.add_constant(train_df[X_cols_2])
    ols2_train = sm.OLS(train_df[y_col].astype(float), X_train_2).fit()
    if len(test_df) > 0:
        X_test_2 = sm.add_constant(test_df[X_cols_2], has_constant="add")
        yhat2_test = ols2_train.predict(X_test_2)
        mape_ols2_test = safe_mape(test_df[y_col].values, yhat2_test.values)
    else:
        mape_ols2_test = np.nan

    X_cols_3 = [t_col, "CPQC", "Q2", "Q3", "Q4"]
    X_cols_3 = [c for c in X_cols_3 if c in train_df.columns]
    X_train_3 = sm.add_constant(train_df[X_cols_3])
    ols3alt_train = sm.OLS(train_df[y_col].astype(float), X_train_3).fit()
    if len(test_df) > 0:
        X_test_3 = sm.add_constant(test_df[X_cols_3], has_constant="add")
        yhat3_test = ols3alt_train.predict(X_test_3)
        mape_ols3alt_test = safe_mape(test_df[y_col].values, yhat3_test.values)
    else:
        mape_ols3alt_test = np.nan

    with open(os.path.join(outdir, "q4_model2_summary.txt"), "w", encoding="utf-8") as f:
        f.write(ols2_train.summary().as_text())
    with open(os.path.join(outdir, "q4_model3_summary.txt"), "w", encoding="utf-8") as f:
        f.write(ols3alt_train.summary().as_text())

    metrics_summary = pd.DataFrame({
        "Model": ["Q1: Trend", "Q2: ETS (Sanluong) in-sample", "Q3: Full multireg in-sample",
                  "Q4-Compare: Model(2) holdout", "Q4-Compare: Model(3) holdout"],
        "MAPE": [safe_mape(y, model_df["yhat_q1"]), mape_q2_y, mape_q3_in, mape_ols2_test, mape_ols3alt_test],
        "Adj_R2": [np.nan, np.nan, ols3.rsquared_adj, ols2_train.rsquared_adj, ols3alt_train.rsquared_adj],
        "AIC": [ols1.aic, np.nan, ols3.aic, ols2_train.aic, ols3alt_train.aic]
    })
    metrics_summary.to_csv(os.path.join(outdir, "metrics_summary.csv"), index=False)

    # Recommendation
    if pd.notna(mape_ols2_test) and pd.notna(mape_ols3alt_test):
        if mape_ols2_test < mape_ols3alt_test:
            rec = "Chọn Model (2) vì MAPE holdout thấp hơn."
        elif mape_ols3alt_test < mape_ols2_test:
            rec = "Chọn Model (3) vì MAPE holdout thấp hơn."
        else:
            rec = "Hai mô hình tương đương theo MAPE holdout; cân nhắc AIC/R² và tính đơn giản."
    else:
        rec = "Không đủ dữ liệu holdout để so sánh khách quan; tham khảo AIC/R² và tính đơn giản."

    # Print key outputs
    print("\n=== Recommendation (Q4) ===")
    print(rec)
    print("\n=== Key Equations ===")
    print(f"Q1: {y_col} = {ols1.params['const']:.4f} + {ols1.params[t_col]:.4f} * t + e")
    print("\n=== Saved outputs in:", outdir, "===\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sav", type=str, required=True, help="Path to the .sav data file")
    parser.add_argument("--h", type=int, default=4, help="Forecast horizon (quarters)")
    parser.add_argument("--outdir", type=str, default="outputs", help="Folder to save outputs")
    args = parser.parse_args()
    main(args)
