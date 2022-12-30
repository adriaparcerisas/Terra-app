#!/usr/bin/env python
# coding: utf-8

# In[79]:


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


# In[80]:


st.title('Activity on Terra')


# In[81]:


st.markdown('The **activity** of a blockchain network is one of the most important things in crypto. Not only because of it is a measure to track the viability of a project but also because of it provides several relevant metrics about the progress of the network and its usage.')


# In[82]:


st.markdown('In this section, we are gonna track the basic metrics registered on **Terra Ecosystem** so far such as:') 
st.write('')
st.write('**_Transactions_**')
st.write('- Average Transaction Fee per txn per week')
st.write('- Total Transaction Fees per week')
st.write('- Total number of transactions per week')
st.write('- Average transactions per second (TPS) per week')
st.write('- Average block time per week')
st.write('')
st.write('**_Wallets_**')
st.write('- Total number of new wallets per week')
st.write('- Total number of active wallets per week')
st.write('- Cumulative number of new wallets per week')


# In[83]:


sql = f"""
SELECT 
  trunc(block_timestamp,'week') as date,
    count(distinct tx_id) as txs,
    sum(txs) over (order by date) as cum_txs,
    avg(txs) over (order by date, date rows between 6 preceding and current row) as ma7_txs,
    avg(txs) over (order by date, date rows between 14 preceding and current row) as ma15_txs,
    avg(txs) over (order by date, date rows between 29 preceding and current row) as ma30_txs,
    sum(TX:body:messages[0]:amount[0]:amount)/pow(10,6) as volume,
    sum(volume) over (order by date) as cum_volume,
    avg(volume) over (order by date, date rows between 6 preceding and current row) as ma7_volume,
    avg(volume) over (order by date, date rows between 14 preceding and current row) as ma15_volume,
    avg(volume) over (order by date, date rows between 29 preceding and current row) as ma30_volume
FROM terra.core.fact_transactions
WHERE tx:body:messages[0]:amount[0]:denom = 'uluna' -- LUNA 2.0 ACTIONS
AND block_timestamp > '2022-05-28' -- LUNA 2.0 LAUNCH
AND tx_succeeded = true
group by 1
order by 1
"""


# In[84]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data
results = compute(sql)
df = pd.DataFrame(results.records)
df.info()
st.subheader('Terra general activity metrics regarding transactions')
st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[85]:


import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Bar(x=df['date'],
                y=df['txs'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                ))
fig.add_trace(go.Line(x=df['date'],
                y=df['ma7_txs'],
                name='7-MA',
                marker_color='rgb(11, 78, 154)'
                ))
fig.add_trace(go.Line(x=df['date'],
                y=df['ma15_txs'],
                name='15-MA',
                marker_color='rgb(247, 203, 115)'
                ))
fig.add_trace(go.Line(x=df['date'],
                y=df['ma30_txs'],
                name='30-MA',
                marker_color='rgb(230, 75, 51)'
                ))

fig.update_layout(
    title='Number of LUNA 2.0 transactions over time',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='# of transactions',
        titlefont_size=16,
        tickfont_size=14,
    ),
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


# In[86]:


sql2 = f"""
--Average Transaction Fee per txn per week
--Total Transaction Fees per week
--Total number of transactions per week
--Average transactions per second (TPS) per week
--Average block time per week
--Wallets
--Total number of new wallets per week
--Total number of active wallets per week
--Cumulative number of new wallets per week
with daily as (
SELECT 
  trunc(block_timestamp,'day') as days,
	count(distinct tx_id) as txs,
  	  txs/84600 as tps,
    sum(txs) over (order by days) as cum_txs,
  	count(distinct tx_sender) as active_users,
  	sum(active_users) over (order by days) as cum_active_users,
  	sum(fee) as total_fees,
  	sum(total_fees) over (order by days) as cum_fees,
  	avg(fee) as avg_tx_fee
FROM terra.core.fact_transactions
WHERE tx:body:messages[0]:amount[0]:denom = 'uluna' -- LUNA 2.0 ACTIONS
AND block_timestamp > '2022-05-28' -- LUNA 2.0 LAUNCH
AND tx_succeeded = true
group by 1
order by 1
  ),
  blocks as (
select
  block_id as block_number,
  min(block_timestamp) as block_debut,
  LAG(block_debut,1) IGNORE NULLS OVER (ORDER BY block_number) as last_block_time
from terra.core.fact_blocks
where block_timestamp > '2022-05-28'
group by 1
--order by 1 asc
  ),
  times as (
SELECT
block_number,
  block_debut,
datediff('second',last_block_time,block_debut) as time_between_blocks_in_sec
from blocks
  ),
  news as (
  SELECT
  distinct tx_sender,
  min(block_timestamp) as debut
  from terra.core.fact_transactions
  group by 1
  ),
  news2 as (
  SELECT
  trunc(debut,'day') as days,
  count(distinct tx_sender) as new_users
  from news group by 1
  )
  
SELECT
trunc(d.days,'week') as date,
avg(avg_tx_fee) as avg_tx_fee_per_week,
avg(txs) as total_weekly_txs,
avg(total_fees) as total_weekly_fees,
avg(tps) as avg_TPS,
avg(time_between_blocks_in_sec) as avg_time_per_block_in_sec,
avg(active_users) as total_weekly_active_users,
avg(new_users) as new_weekly_users,
sum(new_weekly_users) over (order by date) as cum_new_weekly_users
from daily d
join times t on trunc(d.days,'week')=trunc(t.block_debut,'week')
join news2 n on trunc(d.days,'week')=trunc(n.days,'week')
group by 1 
order by 1 asc
"""


# In[87]:


results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()
#st.markdown('Total number of unique users on Near so far')
#st.dataframe(df2)


# In[88]:


fig4 = go.Figure()
fig4.add_trace(go.Bar(x=df2['date'],
                y=df2['total_weekly_fees'],
                name='Weekly fees',
                marker_color='rgb(250, 113, 131)'
                ))
fig4.add_trace(go.Line(x=df2['date'],
                y=df2['avg_tx_fee_per_week'],
                name='Average transaction fee',
                marker_color='rgb(8, 179, 37)'
                ))

fig4.update_layout(
    title='Weekly fees (LUNA)',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Fees in LUNA',
        titlefont_size=16,
        tickfont_size=14,
    ),
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
st.plotly_chart(fig4, theme=None, use_container_width=True)


# In[89]:


fig22 = go.Figure()
fig22.add_trace(go.Line(x=df2['date'],
                y=df2['avg_tps'],
                name='Average TPS',
                marker_color='rgb(153, 14, 175)'
                ))
fig22.add_trace(go.Line(x=df2['date'],
                y=df2['avg_time_per_block_in_sec'],
                name='Average time per block (sec)',
                marker_color='rgb(208, 198, 171)'
                ))

fig22.update_layout(
    title='TPS and TPB',
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
st.plotly_chart(fig22, theme="streamlit", use_container_width=True)


# In[90]:


st.subheader('Terra general activity metrics regarding user activity')
st.markdown('In this first part, we can take a look at the main activity metrics of users on Terra, where it can be seen how the new users come to Terra and how users have interacted with the ecosystem.')


# In[91]:


fig3 = go.Figure()
fig3.add_trace(go.Bar(x=df2['date'],
                y=df2['new_weekly_users'],
                name='New users',
                marker_color='rgb(51, 230, 81)'
                ))
fig3.add_trace(go.Line(x=df2['date'],
                y=df2['cum_new_weekly_users'],
                name='Total new users',
                marker_color='rgb(8, 179, 37)'
                ))

fig3.update_layout(
    title='New LUNA 2.0 users over time',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='# of users',
        titlefont_size=16,
        tickfont_size=14,
    ),
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
st.plotly_chart(fig3, theme=None, use_container_width=True)


# In[92]:


import plotly.graph_objects as go

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df['date'],
                y=df['volume'],
                name='Volume (LUNA)',
                marker_color='rgb(51, 230, 81)'
                ))
fig2.add_trace(go.Line(x=df['date'],
                y=df['ma7_volume'],
                name='7-MA',
                marker_color='rgb(8, 179, 37)'
                ))
fig2.add_trace(go.Line(x=df['date'],
                y=df['ma15_volume'],
                name='15-MA',
                marker_color='rgb(247, 203, 115)'
                ))
fig2.add_trace(go.Line(x=df['date'],
                y=df['ma30_volume'],
                name='30-MA',
                marker_color='rgb(230, 75, 51)'
                ))

fig2.update_layout(
    title='Volume of LUNA 2.0 over time',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Total volume in LUNA',
        titlefont_size=16,
        tickfont_size=14,
    ),
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
st.plotly_chart(fig2, theme=None, use_container_width=True)


# In[ ]:




