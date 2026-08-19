#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from RNgenerator import random_numbers_generator
from Simulator import GBM
from Pricer import LSPricer

#Setting Parameters
S_0=100
K=105
sigma=0.2
r=0.05
T=1
N=252
n_simulations=10000
d_t=T/N

Z = random_numbers_generator(n_simulations ,N ,mode = "Normal")

S_full = GBM(S_0 , r ,T ,N ,n_simulations ,z=Z)

American_C = LSPricer(S_full ,d_t ,r ,sigma ,K ,N ,mode = "Call")
American_P = LSPricer(S_full ,d_t ,r ,sigma ,K ,N ,mode = "Put")

print ("American Call Option =",f"{American_C:.3f}",
       "American Put Option =",f"{American_P:.3f}")

