#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from scipy.stats import qmc , norm

def GBM(S_0 , r ,sigma ,T ,N ,n_simulations ,z):
    d_t =  T/N
    Increment = (r- 0.5*np.square(sigma))*d_t + sigma*np.sqrt(d_t)*z # Define the increment
    cum_increments = np.cumsum(Increment, axis=1) # Cumulative sum of increments
    S_t = S_0 * np.exp(cum_increments)
    S=np.zeros((n_simulations,1)) # Alternative : np.full((n_simulations, 1), S_0)
    S[:,0]=S_0
    S_full = np.hstack((S, S_t))
    
    return(S_full)
    
    
    


# In[ ]:




