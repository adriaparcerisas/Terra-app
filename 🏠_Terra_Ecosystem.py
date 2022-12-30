#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import altair as alt
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[9]:


st.title('Terra Ecosystem Dashboard')


# In[10]:


st.markdown("Fueled by a passionate community and deep developer talent pool, the Terra blockchain is fully community-owned and built to enable the next generation of Web3 products and services [[1]](https://www.terra.money/).")
st.markdown("The events that happened in May 2022 in the world of cryptocurrencies were unprecedented in the history of this asset class; More than 40 billion dollars of capital was lost and many small investors from billion dollar funds suffered losses.")
st.markdown("LUNA's market value was about 30 billion dollars shortly before the collapse. The consequences of what happened to the Terra network and the LUNA currency were so severe that there have been at least 8 confirmed cases of suicide due to capital loss in the Terra ecosystem.")
st.markdown("Creating a stablecoin from almost nothing greatly increases capital efficiency and can bring rapid growth to any ecosystem. Terra's strategy for creating a decentralized stablecoin seemed to be to use the “Growth Hack” to get as big as possible. The main idea of ​​Do Kwon was Anchor, the main protocol of this network and its attractive profit. With the help of attracting stray capital, the rapid growth of the number of Terra network users became possible.")
st.markdown("In the first quarter of 2022, with the collapse of the crypto market, Anchor had become a serious problem for Terra. Billions of dollars that could have been put to other uses and used in other platforms and even in the real world were wasted only to make profit in Anchor smart contracts. Such an attractive profit was even a hindrance to other beneficial projects of the Terra ecosystem. The bear market had reduced demand for loans, and Anchor's reserves were dwindling daily at an alarming rate.")
st.markdown("In March, proposals to cut profits emerged at Anchor's governance forum. It has been revealed that the proposal approved by the Anchor team was a much steeper cut than what was approved, but that Do Kwon personally vetoed it. This brings us to another major problem with Terra's ecosystem; This network was decentralized in name only. The development teams of many of the _independent_ projects in the Terra ecosystem were either directly employed by Terraform Labs or in critical need of its support. To support the Anchor protocol benefit, Terra had to dump LUNA. On the other hand, the issue of buying Bitcoin with the help of selling LUNA was also raised and carried out. To make up for this by _burning Luna_, Do Kwon made perhaps his most fatal mistake; Listing UST on centralized exchanges like Binance and FTX created new demand for UST and burning LUNA. By taking the pricing process further and further out of Terra's control, the situation worsened. Another destructive factor was personality cult, halo effect and maximalism of Do Kwon fans and Terra ecosystem. When bigotry takes the place of logic, critics are marginalized and the power of reason is lost. Evidence of criticism of the Terra ecosystem has been available since 2018. Criticisms that Do Kwon has faced harsh criticism many times [[2]](https://financefeeds.com/understanding-terra-2-0-why-luna-deserves-another-chance/).")


# In[11]:


st.markdown("All of the events discussed eventually led to the creation of a new network called Terra 2 and its native cryptocurrency called LUNA 2. This network and its cryptocurrency was an attempt to revive the Terra ecosystem and compensate the users who faced irreparable losses [[3]](https://app.flipsidecrypto.com/dashboard/flash-bounty-luna-head-YcJtSe).")
st.markdown("Basically, following the demise of the stablecoin, the Terra Luna ecosystem required a fresh new token to be implemented on the new Terra blockchain. This token, known as Luna 2.0, serves that purpose. Do Kwon, the founder of TerraForm Labs, proposed an idea that would see a new chain replace the old Terra network. This idea was given the name _the Luna rebirth_. In conjunction with this, the previous version of Luna was succeeded by Luna 2.0. It has broken ties to the UST stablecoin, which was one of the factors that contributed to the crash in the first place.")
st.markdown("On May 28th, during the genesis block for the new Terra chain, Luna 2.0 was made available to the public. The first block on the new mainnet, which was referred to as Phoenix-1, was produced at the time that was designated as the launch time, which was 6 AM UTC (2 AM ET, 11 PM PT). Terra, who originally planned for this to launch on May 27, has moved this date back one day. On May 27, snapshots for the coin airdropping occurred at Terra Classic block 7790000 [[4]](https://app.flipsidecrypto.com/dashboard/flash-bounty-luna-head-w6759D).")

st.markdown("The main idea of this app is to show an overview of the entire **Terra Ecosystem** through a dive deep analysis of each area of interest. You can find information about each different section by navigating on the sidebar pages.")


# In[12]:


st.markdown("These includes:") 
st.markdown("1. **_Activity_**") 
st.markdown("2. **_Supply_**")
st.markdown("3. **_Staking_**")
st.markdown("4. **_Development_**")

