#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Random numbers generator with notes import random_numbers_generator
from Simulator with notes import GBM
from Pricer with notes import LSPricer

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

S_full = GBM(S_0 , r ,sigma ,T ,N ,n_simulations ,z=Z)

American_C = LSPricer(S_full ,d_t ,sigma ,r ,T ,K ,mode = "Call")
American_P = LSPricer(S_full ,d_t ,sigma ,r ,T ,K ,mode = "Put")

print ("American Call Option =",f"{American_C:.3F}",
       "American Put Option =",f"{American_P:.3F}")

