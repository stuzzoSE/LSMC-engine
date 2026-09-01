#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from numpy.polynomial import Polynomial

def LSPricer(S_full, d_t, r, K, N, mode="Call"):
    if mode == "Call":
        C = np.maximum(S_full[:, -1] - K, 0) 
    elif mode == "Put":                      
        C = np.maximum(K - S_full[:, -1], 0)
    else:
        raise ValueError(f"Unknown mode: {mode}")
        
    for t in range(N - 1, 0, -1): 
        S_t = S_full[:, t] 
        C = C * np.exp(-r * d_t) 
    
        if mode == "Call": 
            itm = S_t > K 
        elif mode == "Put":
            itm = S_t < K 
            
        
        num_itm = np.sum(itm)
        
        
        if num_itm > 2:  
            if mode == "Call":
                Exercise_Value = S_t[itm] - K
            elif mode == "Put":
                 Exercise_Value = K - S_t[itm]
            
            X = S_t[itm] / K
            
            
            poly = Polynomial.fit(X, C[itm], deg=2)
            Continuation_Value = poly(X)  
            
            Exercise_Now = Exercise_Value > Continuation_Value  
            itm_indices = np.where(itm)[0]                                                       
            exercise_indices = itm_indices[Exercise_Now] 
            
            C[exercise_indices] = Exercise_Value[Exercise_Now] 
            
        
        elif num_itm > 0:
            if mode == "Call":
                Exercise_Value = S_t[itm] - K
            elif mode == "Put":
                 Exercise_Value = K - S_t[itm]
                 
            
            Exercise_Now = Exercise_Value > C[itm]
            itm_indices = np.where(itm)[0]
            exercise_indices = itm_indices[Exercise_Now]
            
            C[exercise_indices] = Exercise_Value[Exercise_Now]
    
    C = C * np.exp(-r * d_t)
    return np.mean(C)
            
         
            


# In[ ]:




