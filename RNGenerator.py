#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from scipy.stats import qmc , norm


def random_numbers_generator(n_simulations ,N ,mode = "Normal", seed =None):
    if seed is not None:      
        np.random.seed(seed)
    
    if mode == "Normal":
        z = np.random.normal(0,1,(n_simulations,N)) 
        
    elif mode == "Sobol":
        sobol = qmc.Sobol(d=N,scramble=True,seed=seed) 
        quasi_random_numbers= sobol.random(n_simulations)
        z= norm.ppf(quasi_random_numbers)
        
    elif mode == "AV":
        z_plus = np.random.normal(0,1,(n_simulations//2,N)) #Half the number of simulations because
        z_minus = - z_plus                                  #of the Annntithetic Variates
        z = np.vstack((z_plus,z_minus))
        
    else :
        raise ValueError(f"Unknown mode: {mode}")
        
    return z










# In[ ]:




