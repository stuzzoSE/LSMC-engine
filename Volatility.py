#!/usr/bin/env python
# coding: utf-8

# In[9]:


#!pip install arch
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from DataFetch import Stock_data
from arch import arch_model


def Volatility_RW(ticker ,start , end ,k ,N):  #Rolling window method
    AdjClPrices = Stock_data(ticker ,start ,end)
    log_returns = np.log(AdjClPrices/AdjClPrices.shift(1))
    sigmas_RW =[] 
    for t in range(k ,len(log_returns)):
        sigma_RW_calc = np.sqrt(
            1/(k-1)*np.sum((log_returns[t-k:t] - np.mean(log_returns[t-k:t]))**2))* np.sqrt(N) # The formula()
        sigmas_RW.append(sigma_RW_calc)
        
    return np.array(sigmas_RW)


#We need the BS formula to use the brentq
def Black_Scholes(S_0 ,K ,r , sigma ,T, mode="Call"):
        d_1 = (np.log(S_0 / K) + (r + (sigma**2) / 2) * T) / (sigma * np.sqrt(T))
        d_2=d_1-sigma*np.sqrt(T)
        if mode=="Call":
            return S_0*norm.cdf(d_1)-K*np.exp(-r*T)*norm.cdf(d_2)
        elif mode=="Put":
            return K*np.exp(-r*T)*norm.cdf(-d_2)-S_0*norm.cdf(-d_1)
        
def Implied_Volatility(Market_Value ,S_0, K ,r ,T ,mode="Call"): 
    def objective(sigma):
        return Black_Scholes(S_0 ,K ,r ,sigma ,T , mode=mode) - Market_Value
    
    low_vol, high_vol=1e-4, 5 
    
    try: 
        IV=brentq(objective, low_vol, high_vol)
    except ValueError:
        print("Error")
        IV= None
    return IV


def Volatility_GARCH(ticker , start ,end):
    AdjClPrices = Stock_data(ticker ,start ,end)
    log_returns = np.log(AdjClPrices/AdjClPrices.shift(1)).dropna() 
    
    am = arch_model(log_returns*100, mean='Zero', vol='Garch',p=1, q=1 ,dist='normal')
    res = am.fit(disp ='off') 
    sigma_GARCH = res.conditional_volatility* np.sqrt(252)/100
    return sigma_GARCH


# In[ ]:





# In[ ]:





# In[ ]:




