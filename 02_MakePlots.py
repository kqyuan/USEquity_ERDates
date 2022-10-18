# 
# (Process-driven dev code, not optimized for efficiency.)
#
# 1. Compute quintile dollar growth
# 2. Plot results
#
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
   
day_bef, day_aft = -20, 61
col_day = ["Day_"+str(x) for x in range(day_bef, day_aft, 1)]

df_befaft = pd.read_csv("price_befaft.csv")
list_sector = df_befaft.sort_values(by="GICS Sector")["GICS Sector"].drop_duplicates().to_list()

# Cut Earning Surprise into Quintiles
list_label = ["Q5", "Q4", "Q3", "Q2", "Q1"]
df_befaft["Quintile"] = pd.qcut(df_befaft["Surprise(%)"], q=5, labels=list_label)

df_nominal = df_befaft.groupby(["Quintile"])[col_day].mean().T
df_m = df_befaft[col_day].mean().T
df_rel = df_nominal.subtract(df_m.values, axis=0)

# Simple function to make plots
def plotChart(df_nominal, df_rel, note):
    fig, ax = plt.subplots(1, 2)
    fig.set_figheight(8)
    fig.set_figwidth(16)
    title = f"Price Return Before&After Earnings Report (01/01/2018 to 06/30/2022)\n {note} "
    fig.suptitle(title, fontsize=16)

    x_tics = [x for x in range(day_bef, day_aft, 1)]
    
    # Nominal
    ax[0].plot(x_tics, df_nominal["Q1"].values, lw=2, color="blue",   label="Q1 (Highest Earnings Surprise)")
    ax[0].plot(x_tics, df_nominal["Q2"].values, lw=2, color="green",  label="Q2")
    ax[0].plot(x_tics, df_nominal["Q3"].values, lw=2, color="black",  label="Q3")
    ax[0].plot(x_tics, df_nominal["Q4"].values, lw=2, color="orange", label="Q4")
    ax[0].plot(x_tics, df_nominal["Q5"].values, lw=2, color="red",    label="Q5 (Lowest Earnings Surprise)")
    ax[0].axvline(0, color="black", ls="--")
    ax[0].axhline(1, color="black", ls="--")
    ax[0].grid(axis="both")
    ax[0].set_title("Nominal Price Return by Quintiles")
    ax[0].legend(loc="upper left")
    ax[0].set_xlabel("Trading Days Relative to Earnings Report")
    ax[0].set_ylabel("Nominal Price Return")
    ax[0].set_ylim([0.96, 1.2])
    
    # Relative
    ax[1].plot(x_tics, df_rel["Q1"].values, lw=2, color="blue",   label="Q1 (Highest Earnings Surprise)")
    ax[1].plot(x_tics, df_rel["Q2"].values, lw=2, color="green",  label="Q2")
    ax[1].plot(x_tics, df_rel["Q3"].values, lw=2, color="black",  label="Q3")
    ax[1].plot(x_tics, df_rel["Q4"].values, lw=2, color="orange", label="Q4")
    ax[1].plot(x_tics, df_rel["Q5"].values, lw=2, color="red",    label="Q5 (Lowest Earnings Surprise)")
    ax[1].axvline(0, color="black", ls="--")
    ax[1].axhline(0, color="black", ls="--")
    ax[1].grid(axis="both")
    ax[1].set_title("Relative (to Market or Sector Avg.) Price Return by Quintiles")
    ax[1].legend(loc="upper left")
    ax[1].set_xlabel("Trading Days Relative to Earnings Report")
    ax[1].set_ylabel("Relative Price Return")
    ax[1].set_ylim([-0.06, 0.12])

    return fig

from matplotlib.backends.backend_pdf import PdfPages
pdf = PdfPages("dollar_growth.pdf")

fig = plotChart(df_nominal, df_rel, "SPX: All Sectors")
pdf.savefig(fig)
plt.close()

for isector in list_sector:
    print (isector)
    # Cut Earning Surprise into Quintiles
    df_sector = df_befaft[df_befaft["GICS Sector"]==isector].copy()

    list_label = ["Q5", "Q4", "Q3", "Q2", "Q1"]
    df_sector["Quintile"] = pd.qcut(df_sector["Surprise(%)"], q=5, labels=list_label)
    
    df_nominal = df_sector.groupby(["Quintile"])[col_day].mean().T
    df_m = df_sector[col_day].mean().T
    df_rel = df_nominal.subtract(df_m.values, axis=0)
    fig = plotChart(df_nominal, df_rel, "SPX: "+isector)
    pdf.savefig(fig)
    plt.close()

pdf.close()

