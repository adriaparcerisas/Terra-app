#!/usr/bin/env python
# coding: utf-8

# In[65]:


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


# In[66]:


st.title('Development')


# In[67]:


st.markdown('Contracts are simply programs stored on a blockchain that run when predetermined conditions are met. They typically are used to automate the execution of an agreement so that all participants can be immediately certain of the outcome, without any intermediarys involvement or time loss.')
st.markdown('In blockchain networks, the contracts are one of the most important things because of without them the network would not exists. For that, contracts are the main reason of a blockchain development. When more contracts are used, more large are the blockchain and then more growth could be expected.')


# In[68]:


st.markdown('In this section, we are gonna track the basic metrics regarding development of **Terra Ecosystem** such as:') 
st.write('- Weekly and cumulative new contracts deployed')
st.write('- Stablecoins transfers in and out on the ecosystem')
st.write('- Users transferring stablecoins in and out on the ecosystem')
st.write('- Netflow volume of stablecoins')
st.write('- Average volume deposited and withdrawn')
st.write('')


# In[69]:


sql = f"""
-- Construct a dashboard that displays the number of new contracts deployed 
-- and the total number of contracts deployed each week over the past several months. 
-- Your dashboard should also chart the development of stablecoins, including any supply trends.
with tab1 as (
select 
  distinct tx:body:messages[0]:contract as contract,
  min(block_timestamp) as debut
  from terra.core.fact_transactions 
  --where ATTRIBUTE_KEY in ('contract','u_contract_address','contract_name',
  --'contract_version','contract_addr','contract_address','dao_contract_address','pair_contract_addr','nft_contract')
  group by 1
)
SELECT
trunc(debut,'week') as weeks,
count(distinct contract) as new_contracts,
sum(new_contracts) over (order by weeks) as total_new_contracts
from tab1
group by 1
order by 1 asc 
"""


# In[70]:


st.subheader('Terra contracts development activity')
st.markdown('In this first part, we well take a look at the main development activity carried out on Terra ecosystem such as weekly new and active contracts, most common used contracts, as well as the most common sector used.')
st.markdown('')


# In[71]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data
results1 = compute(sql)
df1 = pd.DataFrame(results1.records)
df1.info()


# In[72]:


import altair as alt
base=alt.Chart(df1).encode(x=alt.X('weeks:O', axis=alt.Axis(labelAngle=325)))
bar=base.mark_bar(color='blue',opacity=0.5).encode(y=alt.Y('new_contracts:Q', axis=alt.Axis(grid=True)))
line=base.mark_line(color='darkblue').encode(y='total_new_contracts:Q')

st.altair_chart((line + bar).resolve_scale(y='independent').properties(title='Daily new deployed contracts over time',width=600))


# In[73]:


sql2="""
-- Construct a dashboard that displays the number of new contracts deployed 
-- and the total number of contracts deployed each week over the past several months. 
-- Your dashboard should also chart the development of stablecoins, including any supply trends.
with tab1 as (
select 
  --distinct tx:body:messages[0]:contract as contract,
  project_name,--label_type,
  min(block_timestamp) as debut,
  count(distinct tx_id) as transactions,
  count(distinct tx_sender) as users
  --from terra.core.fact_msg_attributes x
  from terra.core.dim_address_labels y
  join terra.core.fact_transactions z on address=tx:body:messages[0]:contract
  --where ATTRIBUTE_KEY in ('contract','u_contract_address','contract_name',
  --'contract_version','contract_addr','contract_address','dao_contract_address','pair_contract_addr','nft_contract')
  --and attribute_value not in ('terra1muhks8yr47lwe370wf65xg5dmyykrawqpkljfm39xhkwhf4r7jps0gwl4l','terra1j8hayvehh3yy02c2vtw5fdhz9f4drhtee8p5n5rguvg3nyd6m83qd2y90a','terra1nsuqsk6kh58ulczatwev87ttq2z6r3pusulg9r24mfj2fvtzd4uq3exn26') --avoiding several Astroport contracts
  group by 1
  )
SELECT
*
from tab1
order by 2 asc,3 desc  
"""


# In[74]:


results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[75]:


import plotly.express as px

fig2 = px.bar(df2, x="project_name", y="transactions", color='project_name', color_discrete_sequence=px.colors.qualitative.Antique)
fig2.update_layout(
    title='Top deployed contracts by interactions',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='stack', xaxis={'categoryorder': 'total ascending'},
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
st.plotly_chart(fig2, theme=None, use_container_width=True)


# In[76]:


import plotly.express as px

fig2 = px.bar(df2, x="project_name", y="users", color='project_name', color_discrete_sequence=px.colors.qualitative.Antique)
fig2.update_layout(
    title='Top deployed contracts by users usage',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='stack', xaxis={'categoryorder': 'total ascending'},
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

st.plotly_chart(fig2, theme=None, use_container_width=True)


# In[77]:


sql3="""
-- Construct a dashboard that displays the number of new contracts deployed 
-- and the total number of contracts deployed each week over the past several months. 
-- Your dashboard should also chart the development of stablecoins, including any supply trends.
with tab1 as (
select 
  distinct tx:body:messages[0]:contract as contract,
  label_type as project_name,--label_type,
  min(block_timestamp) as debut,
  count(distinct tx_id) as transactions,
  count(distinct tx_sender) as users
  --from terra.core.fact_msg_attributes x
  from terra.core.dim_address_labels y
  join terra.core.fact_transactions z on address=tx:body:messages[0]:contract
  --where ATTRIBUTE_KEY in ('contract','u_contract_address','contract_name',
  --'contract_version','contract_addr','contract_address','dao_contract_address','pair_contract_addr','nft_contract')
  --and attribute_value not in ('terra1muhks8yr47lwe370wf65xg5dmyykrawqpkljfm39xhkwhf4r7jps0gwl4l','terra1j8hayvehh3yy02c2vtw5fdhz9f4drhtee8p5n5rguvg3nyd6m83qd2y90a','terra1nsuqsk6kh58ulczatwev87ttq2z6r3pusulg9r24mfj2fvtzd4uq3exn26') --avoiding several Astroport contracts
  group by 1,2
)
SELECT
*
from tab1
order by 4 asc,5 desc  
"""


# In[78]:


results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()


# In[79]:


fig3 = px.bar(df3, x="project_name", y="transactions", color='project_name', color_discrete_sequence=px.colors.qualitative.Antique)
fig3.update_layout(
    title='Top deployed contracts sector by interactions',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='stack', xaxis={'categoryorder': 'total ascending'},
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


# In[80]:


fig4 = px.bar(df3, x="project_name", y="users", color='project_name', color_discrete_sequence=px.colors.qualitative.Antique)
fig4.update_layout(
    title='Top deployed contracts sector by users usage',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='stack', xaxis={'categoryorder': 'total ascending'},
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

col1,col2=st.columns(2)
with col1:
    st.plotly_chart(fig3, theme=None, use_container_width=True)
col2.plotly_chart(fig4, theme=None, use_container_width=True)


# In[81]:


st.subheader('Terra stablecoins transfers')
st.markdown('In this second part, we well take a look at the stablecoins activity carried out on **Terra ecosystem** through IBC transfers.')
st.markdown('')


# In[82]:


sql4="""
-- Construct a dashboard that displays the number of new contracts deployed 
-- and the total number of contracts deployed each week over the past several months. 
-- Your dashboard should also chart the development of stablecoins, including any supply trends.
with
t1 as (
select 
  block_timestamp,
  case when currency='ibc/B3504E092456BA618CC28AC671A71FB08C6CA0FD0BE7C8A5B5A3E2DD933CC9E4' then 'axlUSDC' 
  when currency='ibc/CBF67A2BCF6CAE343FDF251E510C8E18C361FC02B23430C121116E0811835DEF' then 'axlUSDT' end as stablecoin,
  case when stablecoin in ('axlUSDC','axlUSDT') then 6 end as decimal,
  amount,
  sender,
  receiver,
  transfer_type,
  tx_id
  from terra.core.ez_transfers x
  where currency in ('ibc/B3504E092456BA618CC28AC671A71FB08C6CA0FD0BE7C8A5B5A3E2DD933CC9E4','ibc/CBF67A2BCF6CAE343FDF251E510C8E18C361FC02B23430C121116E0811835DEF') 
and message_type in ('/ibc.applications.transfer.v1.MsgTransfer','/cosmos.bank.v1beta1.MsgMultiSend','/cosmos.bank.v1beta1.MsgSend')
  ),
t2 as (
  SELECT
  trunc(block_timestamp,'week') as weeks,
  stablecoin,
  count(distinct tx_id) as transfers_in,
  count(distinct sender) as users_depositing,
  sum(amount/pow(10,decimal)) as amount_transferred_in,
  avg(amount/pow(10,decimal)) as avg_amount_transferred_in
  from t1 where transfer_type='IBC_Transfer_In'
  group by 1,2
),
t3 as (
  SELECT
  trunc(block_timestamp,'week') as weeks,
  stablecoin,
  count(distinct tx_id) as transfers_out,
  count(distinct sender) as users_sending,
  sum(amount/pow(10,decimal)) as amount_transferred_out,
  avg(amount/pow(10,decimal)) as avg_amount_transferred_out
  from t1 where transfer_type='IBC_Transfer_Off'
  group by 1,2
)
SELECT
ifnull(t2.weeks,t3.weeks) as date,
ifnull(t2.stablecoin,t3.stablecoin) as stablecoin,
ifnull(transfers_in,0) as transfers_ins,ifnull(transfers_out,0) as transfers_outs, transfers_ins-transfers_outs as net_transfers,
ifnull(users_depositing,0) as users_depositings,ifnull(users_sending,0) as users_sendings,users_depositings-users_sendings as net_users,
ifnull(amount_transferred_in,0) as amount_transferred_ins,ifnull(amount_transferred_out,0) as amount_transferred_outs,amount_transferred_ins-amount_transferred_outs as net_amount_transferred,
ifnull(avg_amount_transferred_in,0) as avg_amount_transferred_ins,ifnull(avg_amount_transferred_out,0) as avg_amount_transferred_outs,avg_amount_transferred_ins-avg_amount_transferred_outs as net_avg_amount_transferred
from t2
full outer join t3 on t2.weeks=t3.weeks and t2.stablecoin=t3.stablecoin
order by 1 asc,2
"""


# In[83]:


st.subheader('Terra contracts development activity')
st.markdown('In this first part, we well take a look at the main development activity carried out on Terra ecosystem such as weekly new and active contracts, most common used contracts, as well as the most common sector used.')
st.markdown('')


# In[84]:


results4 = compute(sql4)
df4 = pd.DataFrame(results4.records)
df4.info()


# In[85]:


fig6 = px.bar(df4, x="date", y="transfers_ins", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig6.update_layout(
    title='Daily IBC transfers IN by stablecoin',
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

fig7 = px.bar(df4, x="date", y="transfers_outs", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig7.update_layout(
    title='Daily IBC transfers OUT by stablecoin',
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
    st.plotly_chart(fig6, theme=None, use_container_width=True)
col6.plotly_chart(fig7, theme=None, use_container_width=True)


# In[86]:


fig8 = px.line(df4, x="date", y="net_transfers", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig8.update_layout(
    title='Netflow IBC transfers',
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
st.plotly_chart(fig8, theme=None, use_container_width=True)


# In[87]:


fig6 = px.line(df4, x="date", y="users_depositings", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig6.update_layout(
    title='Daily users depositing by stablecoin',
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

fig7 = px.line(df4, x="date", y="users_sendings", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig7.update_layout(
    title='Daily users removing by stablecoin',
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
    st.plotly_chart(fig6, theme=None, use_container_width=True)
col6.plotly_chart(fig7, theme=None, use_container_width=True)


# In[88]:


fig8 = px.line(df4, x="date", y="net_users", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig8.update_layout(
    title='Netflow IBC users',
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
st.plotly_chart(fig8, theme=None, use_container_width=True)


# In[89]:


fig6 = px.area(df4, x="date", y="amount_transferred_ins", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig6.update_layout(
    title='Daily volume deposited by stablecoin',
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

fig7 = px.area(df4, x="date", y="amount_transferred_outs", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig7.update_layout(
    title='Daily volume removed by stablecoin',
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
    st.plotly_chart(fig6, theme=None, use_container_width=True)
col6.plotly_chart(fig7, theme=None, use_container_width=True)


# In[90]:


fig8 = px.line(df4, x="date", y="net_amount_transferred", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig8.update_layout(
    title='Netflow IBC volume',
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
st.plotly_chart(fig8, theme=None, use_container_width=True)


# In[91]:


fig6 = px.area(df4, x="date", y="avg_amount_transferred_ins", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig6.update_layout(
    title='Daily average volume deposited by stablecoin',
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

fig7 = px.area(df4, x="date", y="avg_amount_transferred_outs", color="stablecoin", color_discrete_sequence=px.colors.qualitative.Plotly)
fig7.update_layout(
    title='Daily average volume removed by stablecoin',
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
    st.plotly_chart(fig6, theme=None, use_container_width=True)
col6.plotly_chart(fig7, theme=None, use_container_width=True)


# In[ ]:




