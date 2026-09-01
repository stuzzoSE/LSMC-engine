#!/usr/bin/env python
# coding: utf-8

# In[12]:


#!pip install yfinance
import yfinance as yf

def Stock_data(ticker ,start ,end):
    stock_matrix =yf.download(ticker ,start ,end) 
    
    return stock_matrix["Close"] 

def Market_Value(ticker ,target_strike):
    Stock=yf.Ticker(ticker)
    
    if not Stock.options: 
        raise ValueError(f"No option expiration dates found for {ticker}")
        
    expirations = Stock.options 
    target_date = expirations[0] 
    
    chain = Stock.option_chain(target_date)
    #Extract call options DataFrame
    calls_df = chain.calls  # Use chain.puts for put options
    
    option_data = calls_df[calls_df["strike"] == target_strike] 
    
    if option_data.empty:
        raise ValueError(
            f"No call option found for {ticker} with strike {target_strike}"
        )
        
    #Extract C_market
    #1st Option
    c_market_last = option_data["lastPrice"].values[0] 

    #2nd Option.Recommended
    c_market_mid = (option_data["bid"].values[0] + option_data["ask"].values[0]) / 2.0 
    if c_market_mid!=0:
        c_market=c_market_mid
    else:
        c_market=c_market_last
      
    return c_market


# In[ ]:




