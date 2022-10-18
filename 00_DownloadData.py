#
# (Process-driven dev code, not optimized for efficiency.)
#
# Download price and earnings dates from Yahoo Finance.
# The yfinance API is not robust enough to successfully downloading all the data
# in one run. In order to refresh all the data, one needs to record the failed 
# tickers and re-download them.
#
import pandas as pd
import yfinance as yf

# Download SPX constituents from Wiki page.
df_spx_member = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
df_spx_member["Symbol"] = df_spx_member["Symbol"].str.replace('.', '-')
list_spx_member = df_spx_member['Symbol'].tolist()
df_spx_member.to_csv("spx_member.csv", index=False)

#for itkr in list_spx_member:
# test
for itkr in ["AAPL"]:
    print (itkr)
    tkr_obj = yf.Ticker(itkr)
    # Daily price
    try:
        df_price = yf.download(tickers=itkr, period='5y', auto_adjust=True)
        df_price.index = df_price.index.tz_convert(None)
        df_price = df_price.reset_index()
        df_price["Date"] = df_price["Date"].apply(lambda x: x.date())
        df_price.to_csv("./data/price/"+itkr+"_price.csv", index=False)
    except:
        pass
    # ER dates
    try:
        df_er = tkr_obj.get_earnings_dates()
        df_er = df_er.dropna()
        df_er.index = df_er.index.tz_convert(None)
        df_er = df_er.reset_index()
        df_er["Date"]   = df_er["Earnings Date"].apply(lambda x: x.date())
        df_er["Time"]   = df_er["Earnings Date"].apply(lambda x: x.time())
        df_er["BefAft"] = df_er["Earnings Date"].apply(lambda x: "aft" if x.time().hour>=16 else "bef")
        df_er.to_csv("./date/ER_dates/"+itkr+"_er.csv", index=False)
    except:
        print ("Error: ", itkr)
        pass

