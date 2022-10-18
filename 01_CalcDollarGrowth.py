#
# (Process-driven dev code, not optimized for efficiency.)
#
# Calculate stock dollar growth starting 20 trading days before
# the earnings date until 60 trading days after.
#
import pandas as pd
import numpy as np

df_spx = pd.read_csv("./spx_member.csv")
list_tkr = df_spx["Symbol"].to_list()

# Trading days before and after earnings dates
day_bef, day_aft = -20, 61
col_day = ["Day_"+str(x) for x in range(day_bef, day_aft, 1)]
col = ["Symbol", "ER_Date", "EPS Estimate", "Reported EPS", "Surprise(%)"]+col_day
df_befaft = pd.DataFrame(columns = col)

# Testing period for earnings reports
T0, T1 = "2018-01-01", "2022-06-30"
# Loop over all stocks
for tkr in list_tkr:
    print (tkr)
    try:
        df_price = pd.read_csv(f"./data/price/{tkr}_price.csv")
        df_price = df_price.set_index("Date")

        df_er = pd.read_csv(f"./data/ER_dates/{tkr}_er.csv")
        df_er = df_er.set_index("Date")
        df_er = df_er[df_er.index>=T0]
        df_er = df_er[df_er.index<=T1]
        list_date = df_er.index.to_list()

        # Loop over earnings dates
        for i in range(len(list_date)):
            # Find the closest trading date before the earning announcement
            # If ER on Sunday, closest date should be Friday
            date_before_er = df_price[df_price.index<=list_date[i]].index.to_list()[-1]
            if date_before_er == list_date[i]:
                # Assuming announced after market
                irow = df_price.index.get_loc(list_date[i])
                # If before market
                if df_er.iloc[i]["BefAft"] == "bef":
                    irow = irow-1
            else:
                irow = df_price.index.get_loc(date_before_er)

            y = df_price.iloc[irow+day_bef:irow+day_aft]["Close"].values
            y0 = df_price.iloc[irow+day_bef]["Close"]
        
            df_befaft.loc[len(df_befaft)] = [
                tkr,
                df_er.iloc[i]["Earnings Date"],
                df_er.iloc[i]["EPS Estimate"],
                df_er.iloc[i]["Reported EPS"],
                df_er.iloc[i]["Surprise(%)"]
            ] + list(y/y0)
    except:
        print ("Failed: ", tkr)
        pass

# Include GICS sictor and company info
df_befaft = df_befaft.merge(df_spx[["Symbol", "Security", "GICS Sector"]], on="Symbol", how="left") 
# Save results
df_befaft.to_csv("price_befaft.csv", index=False)

