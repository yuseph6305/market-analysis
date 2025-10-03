
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_processing import load_data, resample_agg, rolling_metrics, distribution_stats, detect_outliers, minute_heatmap

def build_report(input_path: str, output_xlsx: str, freq="1min", window=120):
    df = load_data(input_path)
    stats = distribution_stats(df)
    agg = resample_agg(df, freq=freq)
    df_roll = rolling_metrics(df, window=window)
    df_out = detect_outliers(df, z=4.0)
    heat = minute_heatmap(df)

    # Save charts as PNGs (one per figure)
    charts = []
    for sym in df["symbol"].unique():
        sub = agg[agg["symbol"] == sym]
        if len(sub)==0: 
            continue
        
        plt.figure()
        plt.plot(sub["timestamp"], sub["spread_bps_mean"])
        plt.title(f"{sym} - Avg Spread (bps)")
        plt.xlabel("Time"); plt.ylabel("bps")
        p1 = f"{sym}_spread_bps.png"
        plt.tight_layout(); plt.savefig(p1, dpi=150); plt.close()
        charts.append(p1)

        plt.figure()
        plt.plot(sub["timestamp"], sub["mid_mean"])
        plt.title(f"{sym} - Avg Mid")
        plt.xlabel("Time"); plt.ylabel("Price")
        p2 = f"{sym}_mid.png"
        plt.tight_layout(); plt.savefig(p2, dpi=150); plt.close()
        charts.append(p2)

    with pd.ExcelWriter(output_xlsx, engine="xlsxwriter", datetime_format="yyyy-mm-dd hh:mm:ss") as writer:
        df.to_excel(writer, sheet_name="ticks", index=False)
        agg.to_excel(writer, sheet_name="resampled", index=False)
        stats.to_excel(writer, sheet_name="stats", index=False)
        df_roll.to_excel(writer, sheet_name="rolling", index=False)
        df_out.to_excel(writer, sheet_name="outliers", index=False)
        heat.to_excel(writer, sheet_name="heatmap", index=True)

        ws = writer.book.add_worksheet("charts")
        row, col = 0, 0
        for img in charts:
            ws.insert_image(row, col, img, {"x_scale":0.8, "y_scale":0.8})
            if col == 0:
                col = 8
            else:
                col = 0
                row += 20
