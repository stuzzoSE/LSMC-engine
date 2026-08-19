#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

def LSPricer(S_full ,d_t ,sigma ,r ,T ,K ,mode = "Call"):
    if mode == "Call":
        C = np.maximum(S_full[:, -1] - K, 0) # S_full[:, -1] gets ALL paths at time T.Last column.For last row I would S_full[-1]
    elif mode == "Put":                      # Creates the C array depending on mode
        C = np.maximum(K - S_full[:, -1], 0)
    else:
        raise ValueError(f"Unknown mode: {mode}")
        
    for t in range(N - 1, 0, -1): # For backwards loop Longstaff-Schwartz (beginning,end, step)
        S_t = S_full[:, t]  # Gives the required stock price at time t
    
        C = C * np.exp(-r * d_t) # Discounts the array C from above
    
        if mode == "Call": # The loop to choose ITM paths depending on the type of option.
            itm = S_t > K #I make it Boolean(Mask it as TRUE/FALSE). I save it as an array of TRUE/FALSE
        elif mode == "Put":
            itm = S_t < K 
            
        if np.any(itm):  # Only run regression if at least 1 path is ITM
            if mode == "Call":
                Exercise_Value = S_t[itm] - K
            elif mode == "Put":
                 Exercise_Value = K - S_t[itm]
            
        
            #If I put it into brackets [itm] it filters where the above condition is TRUE
            coeffs = np.polyfit(S_t[itm], C[itm], 2) # I find the coefficients by running a 
                                                     #2nd degree(quadratic) regression on the pairs
            Continuation_Value = np.polyval(coeffs,S_t[itm]) # or with these 2 lines p = polynomial(coeffs) 
                                                              #Continuation_Value = p(S_t[itm]) 
            
            Exercise_Now = Exercise_Value > Continuation_Value # Set the condition 
            itm_indices = np.where(itm)[0] # I extract the indices from the ITM paths in an array. np.where() finds TRUE values.
                                           #[0] gives me the first element of the list. We use that because the tuple gives in all dimentions. 
                                           #With [0] we access the first element
            exercise_indices = itm_indices[Exercise_Now] # We name exercise_indices where the condition [Exercise_Now]
        
            # Update cashflows
            C[exercise_indices] = Exercise_Value[Exercise_Now]
    
    C = C * np.exp(-r * d_t)
    return np.mean(C)
            
            
            

