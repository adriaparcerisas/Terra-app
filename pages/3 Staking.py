#!/usr/bin/env python
# coding: utf-8

# In[82]:


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


# In[83]:


st.title('Activity on Terra')


# In[84]:


st.markdown('Staking is one of the most attractive features of the cryptocurrencies and for Terra, is not an exception. Lets take a look at the number of cumulative stakers since the start of this year, as well as the number of LUNA staked.')
st.markdown('The **Terra network** is based on the _Delegated Proof-of-Stake consensus algorithm_, where miners (validators) need to stake a native cryptocurrency LUNA to mine Terra transactions. Delegation mechanism allows anyone who wants to support the network and earn staking rewards to delegate to the chosen validator. Staking rewards are first distributed to validators who take a commission for providing their operations and then are withdrawn individually by delegators [1](https://everstake.medium.com/what-is-luna-and-how-to-stake-it-4ebd15e95730).')


# In[85]:


st.markdown('In this section, we are gonna track the basic staking activity metrics registered on **Terra Ecosystem** so far such as:') 
st.write('- Users staking on Terra')
st.write('- Staking actions done')
st.write('- $LUNA volume staked')
st.write('- Staking rewards')
st.write('')


# In[86]:


sql = f"""
--credit : https://app.flipsidecrypto.com/velocity/queries/47efda77-58e2-4ff4-9221-87240f63b51d
with luna_price as(select
date_trunc('day',RECORDED_HOUR) as date,
avg(CLOSE) as price 
from crosschain.core.fact_hourly_prices
where ID ilike 'terra-luna-2'
group by 1
  ), 
  main as(select
date_trunc('day',BLOCK_TIMESTAMP) as date,
action as type,
count(TX_ID) as stake_txs,
count(DISTINCT DELEGATOR_ADDRESS) as users,
sum(amount) as volume
from terra.core.ez_staking
where TX_SUCCEEDED = TRUE
group by 1,2
  )
select
a.date,
type,
price,
stake_txs,
users,
volume,
sum(stake_txs) over (order by a.date) as cum_txs,
sum(users) over (order by a.date) as cum_users,
sum(volume) over (order by a.date) as cum_volume
from main a 
  join luna_price b on a.date=b.date
"""


# In[87]:


st.subheader('Terra basic staking activity')
st.markdown('In this first part, we well take a look at the main activity carried out on Terra ecosystem such as daily actions, active users and volume staked.')
st.markdown('')


# In[88]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data
results1 = compute(sql)
df1 = pd.DataFrame(results1.records)
df1.info()
##st.subheader('Terra general activity metrics regarding transactions')
##st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[89]:


import plotly.express as px

fig1 = px.bar(df1, x="date", y="users", color="type", color_discrete_sequence=px.colors.qualitative.Antique)
fig1.update_layout(
    title='Users staking $LUNA over time',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


# In[90]:


import plotly.express as px

fig2 = px.area(df1, x="date", y="cum_users", color="type", color_discrete_sequence=px.colors.qualitative.Antique)
fig2.update_layout(
    title='Cumulative users staking $LUNA over time',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

col1,col2=st.columns(2)
with col1:
    st.plotly_chart(fig1, theme=None, use_container_width=True)
col2.plotly_chart(fig2, theme=None, use_container_width=True)


# In[91]:


import plotly.express as px

fig3 = px.bar(df1, x="date", y="stake_txs", color="type", color_discrete_sequence=px.colors.qualitative.Dark2)
fig3.update_layout(
    title='Staking actions over time',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


# In[92]:


import plotly.express as px

fig4 = px.area(df1, x="date", y="cum_txs", color="type", color_discrete_sequence=px.colors.qualitative.Dark2)
fig4.update_layout(
    title='Cumulative staking actions over time',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


col3,col4=st.columns(2)
with col3:
    st.plotly_chart(fig3, theme=None, use_container_width=True)
col4.plotly_chart(fig4, theme=None, use_container_width=True)


# In[93]:


fig5 = px.bar(df1, x="date", y="volume", color="type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig5.update_layout(
    title='$LUNA volume staked over time',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


# In[94]:


fig6 = px.area(df1, x="date", y="cum_volume", color="type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig6.update_layout(
    title='Cumulative $LUNA staked over time',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

col5,col6=st.columns(2)
with col5:
    st.plotly_chart(fig5, theme=None, use_container_width=True)
col6.plotly_chart(fig6, theme=None, use_container_width=True)


# In[95]:


st.subheader('Terra staking rewards')
st.markdown('In this last part, we can take a look at the evolution of the Terra staking rewards delivered in $LUNA for stakers of the ecosystem.')
st.markdown('')


# In[96]:


sql2 = f"""
with luna_price as(
  select
date_trunc('day',RECORDED_HOUR) as date,
avg(CLOSE) as price 
from crosschain.core.fact_hourly_prices
where ID ilike 'terra-luna-2'
group by 1
  ),
  main as (select 
date_trunc('day',block_timestamp) as date,
RECEIVER,
TX_ID,
sum(AMOUNT)/pow(10,6) as luna_reward
from terra.core.ez_transfers
where MESSAGE_VALUE['@type'] ='/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward'
and CURRENCY ilike 'uluna'
and TX_SUCCEEDED = TRUE
group by 1,2,3
  )
  
select 
m.date,
count(DISTINCT tx_id) as rewards,
count(DISTINCT RECEIVER) as reward_receivers,
sum(luna_reward) as reward_volume_luna,
sum(luna_reward*price) as reward_volume_usd,
  sum(reward_volume_luna) over (order by m.date) as cum_vol_luna,
  sum(reward_volume_usd) over (order by m.date) as cum_vol_usd
from main m 
  join luna_price l on m.date=l.date
group by 1
"""


# In[97]:


results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[98]:


import altair as alt
base=alt.Chart(df2).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_line(color='darkblue').encode(y=alt.Y('rewards:Q', axis=alt.Axis(grid=True)))
bar=base.mark_line(color='orange').encode(y='reward_receivers:Q')

st.altair_chart((line + bar).resolve_scale(y='independent').properties(title='Daily rewards and receivers over time',width=600))


# In[99]:


base=alt.Chart(df2).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_bar(color='green',opacity=0.5).encode(y=alt.Y('reward_volume_luna:Q', axis=alt.Axis(grid=True)))
bar=base.mark_line(color='darkgreen').encode(y='cum_vol_luna:Q')

st.altair_chart((line + bar).resolve_scale(y='independent').properties(title='Daily volume rewarded (LUNA)',width=600))


# In[100]:


sql3 = f"""
with SEND as(
  select 
sender,
sum(amount) as sent_volume
from terra.core.ez_transfers
where CURRENCY ilike 'uluna'
group by sender
  ),
  
  RECEIVE as(
  select 
receiver,
sum(amount) as received_volume
from terra.core.ez_transfers
where CURRENCY ilike 'uluna'
group by receiver
),

final as (
select  
sender as user, 
(received_volume-sent_volume)/pow(10,6) as balance
from send s 
  join receive r on s.sender=r.receiver 
order by balance desc
)
select
case when balance >1000000 then 'A. >1M'
when balance between 10000 and 1000000 then 'B. 10k-1M'
when balance between 1000 and 10000 then 'C. 1k-10k'
when balance between 100 and 1000 then 'D. 100-1k'
when balance between 10 and 100 then 'E. 10-100'
else 'F. <10' end as balance,
count(distinct user) as users
from final
group by 1 order by 1
"""


# In[101]:


results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.markdown('Total number of unique users on Near so far')
#st.dataframe(df2)


# In[102]:


st.subheader('$LUNA holders')
st.markdown('This final chart represents the distribution of LUNA holders by its balances. The groups are determined by an specific range of LUNA holdings.')
st.markdown('')


# In[103]:


fig = px.funnel(df3, x='users', y='balance')
fig.update_layout(
    title='Distribution of $LUNA holders',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


# In[ ]:




