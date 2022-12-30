#!/usr/bin/env python
# coding: utf-8

# In[88]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[89]:


st.title('Supply on Terra')


# In[90]:


st.markdown('**Supply** is a total amount of coins that can be issued. There are several terms in crypto related to that. Some of the most important terms are the following:')
st.markdown('- Total supply: amount of already issued coins')
st.markdown('- Circulating supply: amount of coins circulating and market. It means that these coins available.')
st.markdown('- Maximum supply : maximum limit of coins that can be issues.')


# In[91]:


st.markdown('In this section, we are gonna track the basic supply metrics registered on **Terra Ecosystem** so far such as:') 
st.write('- Total Supply')
st.write('- Circulating Supply')
st.write('- Vesting Schedule')
st.write('')


# In[92]:


sql = f"""
with SEND as 
(select SENDER,
  sum(AMOUNT) as sent_amount
from 
terra.core.ez_transfers
WHERE
CURRENCY ilike 'uluna'
group by SENDER
  ),
  
RECEIVE as 
(select RECEIVER,
  sum(AMOUNT) as received_amount
from 
terra.core.ez_transfers
WHERE
CURRENCY ilike 'uluna'
group by RECEIVER
  ),

total_supp as (select sum(received_amount)/1e4 as total_supply 
  from RECEIVE r 
  left join SEND s on r.RECEIVER=s.SENDER 
  where sent_amount is null),

t1 as
(select date_trunc('day',BLOCK_TIMESTAMP) as date,
sum(case when FROM_CURRENCY ilike 'uluna' then FROM_AMOUNT/1e6 else null end) as from_amountt,
sum(case when to_CURRENCY ilike 'uluna' then FROM_AMOUNT/1e6 else null end) as to_amountt,
from_amountt-to_amountt as circulating_volume
from
  terra.core.ez_swaps
group by 1
), 
  t3 as (select 
sum(circulating_volume) over (order by date) as circulating_supply ,
  DATE from t1
  )

select total_supply,circulating_supply,  circulating_supply*100/total_supply as ratio 
  from t3 join total_supp
where 
date=CURRENT_DATE
"""


# In[93]:


st.subheader('Terra circulating supply')
st.markdown('In this first part, we well take a look at the current $LUNA circulating supply and its ratio against the total supply.')
st.markdown('')


# In[95]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data
results = compute(sql)
df = pd.DataFrame(results.records)
df.info()
##st.subheader('Terra general activity metrics regarding transactions')
##st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[96]:


import math

millnames = ['',' k',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


# In[97]:


col1,col2,col3=st.columns(3)
with col1:
    st.metric('Total $LUNA Supply', millify(df['total_supply'][0]))
col2.metric('Total Circulating Supply', millify(df['circulating_supply'][0]))
col3.metric('$LUNA Circulating Supply Ratio',round(df['ratio'][0],2))


# In[98]:


sql2 = f"""
with SEND as 
(select SENDER,
  sum(AMOUNT) as sent_amount
from 
terra.core.ez_transfers
WHERE
CURRENCY ilike 'uluna'
group by SENDER
  ),
  
RECEIVE as 
(select RECEIVER,
  sum(AMOUNT) as received_amount
from 
terra.core.ez_transfers
WHERE
CURRENCY ilike 'uluna'
group by RECEIVER
  ),

total_supp as (select sum(received_amount)/1e4 as total_supply 
  from RECEIVE r 
  left join SEND s on r.RECEIVER=s.SENDER 
  where sent_amount is null),

t1 as
(select date_trunc('day',BLOCK_TIMESTAMP) as date,
sum(case when FROM_CURRENCY ilike 'uluna' then FROM_AMOUNT/1e6 else null end) as from_amountt,
sum(case when to_CURRENCY ilike 'uluna' then FROM_AMOUNT/1e6 else null end) as to_amountt,
from_amountt-to_amountt as circulating_volume
from
  terra.core.ez_swaps
group by 1
), 
  t3 as (select 
sum(circulating_volume) over (order by date) as circulating_supply ,
  DATE from t1
  ),

  luna_price as(select
date_trunc('day',RECORDED_HOUR) as date,
avg(CLOSE) as price 
from crosschain.core.fact_hourly_prices
where ID ilike 'terra-luna-2'
group by 1)

select t3.date,circulating_supply,price
  from t3 join luna_price on t3.date=luna_price.date
"""


# In[99]:


results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[100]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['circulating_supply'],
                name='Total $LUNA',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['price'],
                name='USD price',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily $LUNA Circulating Supply vs $LUNA Price',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="$LUNA circulating", secondary_y=False)
fig2.update_yaxes(title_text="$LUNA price", secondary_y=True)
st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


# In[101]:


import plotly.express as px
fig = px.ecdf(df2, x=["circulating_supply"])
fig.update_layout(
    title='ECDF of $LUNA circulating supply',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


# In[102]:


sql3 = f"""
SELECT
  5000000 * (6 / (1654128000 - 1654041600)) as tokens_vested_per_block,
  tokens_vested_per_block * (86400 / 6) as total_vesting_tokens,
1000000 * (6 / 14400) as tokens_vested_per_block_period1,
2000000 * (6 / 21600) as tokens_vested_per_block_period2,
2000000 * (6 / 50400) as tokens_vested_per_block_period3
"""


# In[103]:


results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.markdown('Total number of unique users on Near so far')
#st.dataframe(df2)


# In[104]:


st.subheader('Terra vesting schedule')
st.markdown('In this last part, we can take a look at the main vesting period of $LUNA tokens on Terra ecosystem.')
st.markdown('')
st.subheader('How vesting works?')
st.markdown('Individuals who previously held **LUNA Classic** (LUNA on the original Terra blockchain) will be entitled to a specified number of LUNA tokens on the new Terra blockchain based on the quantity of their holdings at specified snapshots of time. _30%_ of LUNA tokens received will be liquid and may be traded and transferred immediately upon receipt. _70%_ of these tokens will be vesting, meaning that these funds will be available in ones personal wallet, but may not be traded or transfered until a specified period of time. However, these funds may be delegated to validators at any time if the user chooses to do so. Vesting tokens will be stored in a type of vesting account available in ones wallet. Vesting tokens will become vested, or available for trade and transfer, based on a predetermined schedule. We will go over 3 different types of vesting accounts, each with its own unique vesting schedule. [1](https://docs.terra.money/develop/vesting/)')


# In[105]:


st.markdown('- In a continous vesting account, a number of tokens will be vested per block based on a predetermined start and end time. One would have to wait until the specified start time for their tokens to start to become vested. At this point, tokens become vested per block until the end time is reached based on the following equation:')


# In[106]:


st.metric('Tokens vested per block',df3['tokens_vested_per_block'][0])


# In[107]:


st.markdown('- Periodic vesting accounts work similarly to continuous vesting accounts except that vesting occurs over predefined vesting periods. Each period has a specified length corresponding to the number of seconds the period will last.')


# In[108]:


col1,col2,col3=st.columns(3)
with col1:
    st.metric('Period 1 tokens vested/block', df3['tokens_vested_per_block_period1'][0])
col2.metric('Period 2 tokens vested/block',df3['tokens_vested_per_block_period2'][0])
col3.metric('Period 3 tokens vested/block',df3['tokens_vested_per_block_period3'][0])


# In[ ]:




