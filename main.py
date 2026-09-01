#!/usr/bin/env python
# coding: utf-8

# In[1]:


from RNGenerator import random_numbers_generator
from Simulator import GBM
from Pricer import LSPricer
from Volatility import Volatility_RW, Implied_Volatility , Volatility_GARCH
from DataFetch import Market_Value
from Greeks import calculate_greeks

#Setting Parameters
ticker ,start ,end , k = 'NVO' ,'2024-08-26' ,'2026-08-26' ,30
S_0 ,K ,r ,T ,N =55 ,60 ,0.05 ,1 ,252
n_simulations=10000
d_t=T/N


#Fetch Data
market_price=Market_Value(ticker ,target_strike=K)
# Volatility
sigmas = {
    "RW": Volatility_RW(ticker, start, end, k, N)[-1],
    "IV": Implied_Volatility(market_price, S_0, K, r, T, mode="Call"),
    "GARCH": Volatility_GARCH(ticker, start, end).iloc[-1]
}
#RNGenerator
Z = random_numbers_generator(n_simulations ,N ,mode = "Normal")

results = {} 
#Pricer and Greeks
for model, sigma_val in sigmas.items():
    call_greeks = calculate_greeks(S_0, r, sigma_val, T, N, n_simulations, K, z=Z, mode="Call")
    put_greeks  = calculate_greeks(S_0, r, sigma_val, T, N, n_simulations, K, z=Z, mode="Put")
    
    results[model] = {
        "Sigma": sigma_val,
        "Call": call_greeks,
        "Put": put_greeks
    }

print("\n" + "="*70)
print(f"{'Model':<8} | {'Option':<5} | {'Price':<7} | {'Delta':<7} | {'Gamma':<7} | {'Vega':<7}")
print("="*70)
for model, res in results.items():
    for opt_type in ["Call", "Put"]:
        g = res[opt_type]
        print(f"{model:<8} | {opt_type:<5} | ${g['Base Price']:<6.3f} | {g['Delta']:<7.4f} | {g['Gamma']:<7.4f} | {g['Vega']:<7.4f}")

   


# In[ ]:





# In[ ]:




