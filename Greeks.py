#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from Simulator import GBM
from Pricer import LSPricer

def calculate_greeks(S_0, r, sigma, T, N, n_simulations, K, z, mode="Call"):
    d_t = T / N
    
    #
    dS = 0.01 * S_0         # 1% move in stock price
    d_sigma = 0.01          # 1% volatility increase. Plain number
    
    # 2. Simulate paths using the same Z matrix (CRN)
    S_base     = GBM(S_0, r, sigma, T, N, n_simulations, z=z)
    S_up       = GBM(S_0 + dS, r, sigma, T, N, n_simulations, z=z)
    S_down     = GBM(S_0 - dS, r, sigma, T, N, n_simulations, z=z)
    S_vol_up   = GBM(S_0, r, sigma + d_sigma, T, N, n_simulations, z=z)
    S_vol_down = GBM(S_0, r, max(sigma - d_sigma, 1e-4), T, N, n_simulations, z=z)
    
    # 3. Price paths
    P_base     = LSPricer(S_base, d_t, r, K, N, mode=mode)
    P_up       = LSPricer(S_up, d_t, r, K, N, mode=mode)
    P_down     = LSPricer(S_down, d_t, r, K, N, mode=mode)
    P_vol_up   = LSPricer(S_vol_up, d_t, r, K, N, mode=mode)
    P_vol_down = LSPricer(S_vol_down, d_t, r, K, N, mode=mode)
    
    # 4. Finite Difference Formulas
    delta = (P_up - P_down) / (2 * dS)
    gamma = (P_up - 2 * P_base + P_down) / (dS ** 2)
    vega  = (P_vol_up - P_vol_down) / (2 * d_sigma)
    
    return {
        "Base Price": P_base,
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega
    }
    
    

