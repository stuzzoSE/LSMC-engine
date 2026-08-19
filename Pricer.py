#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

def LSPricer(S_full ,d_t ,r ,K ,N ,mode = "Call"):
    if mode == "Call":
        C = np.maximum(S_full[:, -1] - K, 0) 
    elif mode == "Put":                      # Creates the C payoff array depending on mode
        C = np.maximum(K - S_full[:, -1], 0)
    else:
        raise ValueError(f"Unknown mode: {mode}")
        
    for t in range(N - 1, 0, -1): # For backwards loop Longstaff-Schwartz
        S_t = S_full[:, t] 
    
        C = C * np.exp(-r * d_t) # Discounts the payoff array
    
        if mode == "Call": # The loop to choose ITM paths
            itm = S_t > K #I mask it as Boolean
        elif mode == "Put":
            itm = S_t < K 
            
        if np.any(itm):  # Only run regression if at least 1 path is ITM
            if mode == "Call":
                Exercise_Value = S_t[itm] - K
            elif mode == "Put":
                 Exercise_Value = K - S_t[itm]
            
        
            coeffs = np.polyfit(S_t[itm], C[itm], 2) 
                                                     
            Continuation_Value = np.polyval(coeffs,S_t[itm])  
            
            Exercise_Now = Exercise_Value > Continuation_Value # Set the condition 
            itm_indices = np.where(itm)[0] # I extract the indices from the ITM paths in an array. np.where() finds TRUE values.
                                           
            exercise_indices = itm_indices[Exercise_Now] 
        
            C[exercise_indices] = Exercise_Value[Exercise_Now] # Update cashflows
    
    C = C * np.exp(-r * d_t)
    return np.mean(C)
            
            
            

