#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from scipy.stats import qmc , norm

#Create a function/class that I will call on my main script code.
#I will probably call it once in the begginning
def random_numbers_generator(n_simulations ,N ,mode = "Normal", seed =None):
    if seed is not None:      
        np.random.seed(seed)
    
    if mode == "Normal":
        z = np.random.normal(0,1,(n_simulations,N)) #Normal random numbers generator
                                                       # I need matrix that is why the third argumnt gives me a matrix.
                                                       #If only  n_simulations it would create an array
    elif mode == "Sobol":
        sobol = qmc.Sobol(d=N,scramble=True) #Define the Solver
        quasi_random_numbers= sobol.random(n_simulations) #Use the solver for a number of simulations
        z= norm.ppf(quasi_random_numbers) #Inverse CDF
        
    elif mode == "AV":
        z_plus = np.random.normal(0,1,(n_simulations//2,N)) #Half the number of simulations because
        z_minus = - z_plus                                  #of the AV
        z = np.vstack((z_plus,z_minus))
        
    else :
        raise ValueError(f"Unknown mode: {mode}")
        
    return z









# In[ ]:




