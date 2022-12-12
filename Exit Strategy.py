#!/usr/bin/env python
# coding: utf-8

# # Exit multileg options code
#     
# <b> Pocedure:
#     
#     1. Get live data of premiums
#     
#     2. if conditions
#    
#     3. code runs till market closes 
#     
#     

# # IMPORT FILES

# In[1]:


# import files

import schedule
import time

from upstox_api.api import *


# # USER INPUT

# In[2]:


############## USER INPUT ###########################

capital = 100000

short_avg_price = 100
long_avg_price = 50
quantities = 75

short_leg_strike_price = ""
long_leg_strike_price = ""

check = False


# # UPSTOX SETUP
#         
#     1. Create a Session object with your api_key, redirect_uri and api_secret
#     
#     2. Get the login URL so you can login with your Upstox UCC ID and password.
#     
#     3. Login to the URL and set the code returned by the login response in your Session object
#     
#     4. Retrieve your access token
#     
#     5. Establish a session
#     
#     6. Get master contracts

# <b> 1. Create a Session object with your api_key, redirect_uri and api_secret

# In[3]:


# s = Session ('your_api_key')
# s.set_redirect_uri ('your_redirect_uri')
# s.set_api_secret ('your_api_secret')

s = Session ('your_api_key')
s.set_redirect_uri ('your_redirect_uri')
s.set_api_secret ('your_api_secret')


# <b> 2. Get the login URL so you can login with your Upstox UCC ID and password.

# In[4]:


print (s.get_login_url())


# <b> 3. Login to the URL and set the code returned by the login response in your Session object

# In[5]:


# s.set_code ('your_code_from_login_response')

s.set_code ('your_code_from_login_response')


# <b> 4. Retrieve your access token

# In[6]:


access_token = s.retrieve_access_token()
print ('Received access_token: %s' % access_token)


# <b> 5. Establish a session

# In[ ]:


# u = Upstox ('your_api_key', access_token)

u = Upstox ('your_api_key', access_token)


# <b> 6. Get master contracts

# In[ ]:


# Getting master contracts allow you to search for instruments by symbol name and place orders. 
# Whenever you get a trade update, order update, or quote update, the library will check if master contracts are loaded. 
# If they are, it will attach the instrument object directly to the update.

u.get_master_contract('NSE_EQ') # get contracts for NSE EQ
u.get_master_contract('NSE_FO') # get contracts for NSE FO
u.get_master_contract('NSE_INDEX') # get contracts for NSE INDEX
u.get_master_contract('BSE_EQ') # get contracts for BSE EQ
u.get_master_contract('BCD_FO') # get contracts for BCD FO
u.get_master_contract('BSE_INDEX') # get contracts for BSE INDEX
u.get_master_contract('MCX_INDEX') # get contracts for MCX INDEX
u.get_master_contract('MCX_FO') # get contracts for MCX FO


# # EXIT CRITERIA 

# In[ ]:


# Exit Criteria

def exit():
    
    
    # live prices for each leg # 120 # 60
    short_leg_live_mrkt_price = u.get_live_feed(u.get_instrument_by_symbol('NSE_FO', short_leg_strike_price), LiveFeedType.LTP)
    long_leg_live_mrkt_price = u.get_live_feed(u.get_instrument_by_symbol('NSE_FO', long_leg_strike_price), LiveFeedType.LTP)
    
    # MTM 
    MTM_short_leg = quantities * (short_avg_price - short_leg_live_mrkt_price)
    MTM_long_leg = quantities * (-(long_avg_price - long_leg_live_mrkt_price))
    
    # Total PNL
    total_PNL = MTM_short_leg + MTM_long_leg
    
    # exit order conditions #-750 
    # (-(0.018 * capital))
    
    if(total_PNL <= (-(0.018 * capital))):
        
        print("Stop Loss hit!")
        exit_order() 


# # EXIT POSITIONS

# In[ ]:


# Exit orders 

def exit_order():
    
    # Exit short position
    print (u.get_profile())
    u.get_master_contract('nse_fo') # get contracts for NSE EQ

    # TransactionType.Buy, OrderType.Market, ProductType.Delivery

    print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(
       u.place_order(TransactionType.Buy,  #transaction_type
                  u.get_instrument_by_symbol('NSE_FO', short_leg_strike_price),  #instrument
                  quantities,  # quantity
                  OrderType.Market,  # order_type
                  ProductType.Delivery,  # product_type
                  0.0,  # price
                  None,  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY, # duration
                  None, # stop_loss
                  None, # square_off
                  None )# trailing_ticks
       )
    
    # 1 Second gap
    time.sleep(1.2)
    
    
    # Exit long position
    print (u.get_profile())
    u.get_master_contract('nse_fo') # get contracts for NSE EQ

    # TransactionType.Sell, OrderType.Market, ProductType.Delivery

    print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(
       u.place_order(TransactionType.Sell,  #transaction_type
                  u.get_instrument_by_symbol('NSE_FO', long_leg_strike_price),  #instrument
                  quantities,  # quantity
                  OrderType.Market,  # order_type
                  ProductType.Delivery,  # product_type
                  0.0,  # price
                  None,  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY, # duration
                  None, # stop_loss
                  None, # square_off
                  None )# trailing_ticks
       )
    
    
    
    # All orders exectued
    check = True
    print("Order's Executed")


# In[ ]:


print(exit())


# # RETRIEVING LIVE DATA EVERY SECOND

# In[ ]:


# Retrieving live option data every 0.1 seconds

schedule.every(0.1).seconds.do(exit)

# runs until order is executed
while check == False:
     schedule.run_pending()
    time.sleep(0.1)

