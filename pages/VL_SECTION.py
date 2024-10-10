import pandas as pd 
import streamlit as st 
import os
import gspread
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import traceback
import time
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(
    page_title = 'VL SECTION',
    page_icon =":bar_chart"
    )

#st.header('CODE UNDER MAINTENANCE, TRY AGAIN TOMORROW')
#st.stop()
cola,colb,colc = st.columns([1,3,1])
colb.subheader('VIRAL LOAD COVERAGE')

today = datetime.now()
todayd = today.strftime("%Y-%m-%d")# %H:%M")
wk = today.strftime("%V")
week = int(wk)-39
cola,colb = st.columns(2)
cola.write(f"**DATE TODAY:    {todayd}**")
colb.write(f"**CURRENT WEEK:    {week}**")
k = int(wk)

if 'vl' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'VL', usecols=list(range(24)),ttl=5)
        df = exist.dropna(how='all')
        st.session_state.vl = df
     except exception as e:
         st.write(f'{e}')
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dftx = st.session_state.vl.copy()


#REPORTING RATES
@st.cache_data
def report():
    df = pd.read_csv('CLUSTERS.csv')
    df['Q4 CUR'] = pd.to_numeric(df['Q4 CUR'], errors='coerce')
    df = df[df['Q4 CUR']>0].copy()
    return df  

dfrep = report()

#######################FILTERS
clusters = dfrep['CLUSTER'].unique()
weeks = dftx['SURGE'].unique()

fac = dftx['FACILITY'].unique()
#TO USE WHERE WEEKS ARE NOT NEEDED FOR TX
dfy = []
for every in fac:
    dff = dftx[dftx['FACILITY']== every]
    dff = dff.drop_duplicates(subset=['FACILITY'], keep = 'last')
    dfy.append(dff)
water = pd.concat(dfy)

#REMOVE DUPLICATES FROM VL SHEET # HOLD THIS IN SESSION LATER
dfs=[]   
for each in weeks:
    dftx['SURGE'] = pd.to_numeric(dftx['SURGE'], errors='coerce')
    dfa = dftx[dftx['SURGE']==each]
    dfa = dfa.drop_duplicates(subset=['FACILITY'], keep = 'last')
    dfs.append(dfa)
dftx = pd.concat(dfs)


#FILTERS
st.sidebar.subheader('**Filter from here**')
CLUSTER = st.sidebar.multiselect('CHOOSE A CLUSTER', clusters, key='a')

#create for the state
if not CLUSTER:
    dfrep2 = dfrep.copy()
    dftx2 = dftx.copy()
    water2 = water.copy()

else:
    dfrep['CLUSTER'] = dfrep['CLUSTER'].astype(str)
    dfrep2 = dfrep[dfrep['CLUSTER'].isin(CLUSTER)]

    dftx['CLUSTER'] = dftx['CLUSTER'].astype(str)
    dftx2 = dftx[dftx['CLUSTER'].isin(CLUSTER)]
    
    water['CLUSTER'] = water['CLUSTER'].astype(str)
    water2 = water[water['CLUSTER'].isin(CLUSTER)]

district = st.sidebar.multiselect('**CHOOSE A DISTRICT**', dfrep2['DISTRICT'].unique(), key='b')
if not district:
    dfrep3 = dfrep2.copy()
    dftx3 = dftx2.copy()
    water3 = water2.copy()
else:
    dfrep2['DISTRICT'] = dfrep2['DISTRICT'].astype(str)
    dfrep3 = dfrep2[dfrep2['DISTRICT'].isin(district)]

    dftx2['DISTRICT'] = dftx2['DISTRICT'].astype(str)
    dftx3 = dftx2[dftx2['DISTRICT'].isin(district)]
    
    water2['DISTRICT'] = water2['DISTRICT'].astype(str)
    water3 = water2[water2['DISTRICT'].isin(district)]

facility = st.sidebar.multiselect('**CHOOSE A FACILITY**', dfrep3['FACILITY'].unique(), key='c')
if not facility:
    dfrep4 = dfrep3.copy()
    dftx4 = dftx3.copy()
    water4 = water3.copy()
else:
    dfrep4 = dfrep3[dfrep3['FACILITY'].isin(facility)]
    dftx4 = dftx3[dftx3['FACILITY'].isin(facility)]
    water4 = water3[water3['FACILITY'].isin(facility)]


# Base DataFrame to filter
dfrep = dfrep4.copy()
dftx = dftx4.copy()
water = water4.copy()

# Apply filters based on selected criteria
if CLUSTER:
    dfrep = dfrep[dfrep['CLUSTER'].isin(CLUSTER)]
    dftx = dftx[dftx['CLUSTER'].isin(CLUSTER)]

if district:
    dfrep = dfrep[dfrep['DISTRICT'].isin(district)]
    dftx = dftx[dftx['DISTRICT'].isin(district)]
if facility:
    dfrep = dfrep[dfrep['FACILITY'].isin(facility)]
    dftx = dftx[dftx['FACILITY'].isin(facility)]
# #HIGHEST TXML 

st.divider()
#VL COVERAGE

HAVE = water['HAVE'].sum()
NOT = water['NOVL'].sum()
TOTAL = int(HAVE) + in(NOT)

labels = ['HAVE VL', 'DUE']
values = [HAVE, NOT]
# Specify custom colors
colors = ['darkblue', 'red']  # Colors for NO_MMD and MMD
# Create the 3D pie chart
figp = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.3,  # Creates a donut chart (0 for a full pie)
    textinfo='label+percent',  # Show labels and percentages
    pull=[0.1, 0],  # Slightly pull both slices for emphasis
    marker=dict(colors=colors)
)])

# Update layout for 3D effect
figp.update_traces(textposition='inside', textinfo='percent+label')
st.markdown(f'**{TOTAL} ACTIVE CLIENTS, {HAVE} ARE BLED, {NOT} ARE NOT BLED**')
if facility and not district and not CLUSTER:
    st.write(f'**SHOWING DATA FOR {facility} facility**')
st.plotly_chart(figp, use_container_width=True)

#############################################################################################
#LINE GRAPHS
st.divider()
#TREND OF VL COVERAGE
st.write('**TRENDS IN VL COVERAGE**')

grouped = dftx.groupby('SURGE').sum(numeric_only=True).reset_index()

melted = grouped.melt(id_vars=['SURGE'], value_vars=['HAVE', 'NOVL'],
                            var_name='INTERVAL', value_name='Total')

melted2 = grouped.melt(id_vars=['SURGE'], value_vars=['HAVE', 'NOVL'],
                            var_name='CATEGORY', value_name='Total')
melted['SURGE'] = melted['SURGE'].astype(int)
melted['SURGE'] = melted['SURGE'].astype(str)
melted2['SURGE'] = melted2['SURGE'].astype(int)
melted2['SURGE'] = melted2['SURGE'].astype(str)

fig2 = px.line(melted, x='SURGE', y='Total', color='INTERVAL', markers=True,
              title='', labels={'SURGE':'WEEK', 'Total': 'No. of clients', 'INTERVAL': 'INTERVALS'})
fig2.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)
fig2.update_xaxes(type='category')

st.plotly_chart(fig2, use_container_width= True)


#############################################################################################


st.divider()
st.write('**VL COVERAGE IN MISSED APPTS, 1 YR COHORT AND 6 MTHS COHORT**')
pied = water.copy()#[filtered_df['WEEK']==k]
#pied['LOST NEW'] = pied['ORIGINAL COHORT']- pied['ONE YEAR ACTIVE'] 
pied = pied[['WVLY', 'NVLY']]
pied = pied.rename(columns={'WVLY':'BLED', 'NVLY':'DUE'})
melted = pied.melt(var_name='Category', value_name='values')
figY = px.pie(melted, values= 'values', title='ONE YEAR', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'DUE': 'red', 'BLED': 'blue'} )

#pied['LOST NEW'] = pied['ORIGINAL COHORT']- pied['ONE YEAR ACTIVE'] 
pied = water.copy()
pied = pied[['WVLS', 'NVLS']]
pied = pied.rename(columns={'WVLS':'BLED', 'NVLS':'DUE'})
melted = pied.melt(var_name='Category', value_name='values')
fig6 = px.pie(melted, values= 'values', title='6 MTHS', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'DUE': 'red', 'BLED': 'yellow'} )
#pied['LOST NEW'] = pied['ORIGINAL COHORT']- pied['ONE YEAR ACTIVE']
pied = water.copy() 
pied = pied[['LNVL', 'LWVL']]
pied = pied.rename(columns={'LNVL':'DUE', 'LWVL':'BLED'})
melted = pied.melt(var_name='Category', value_name='values')
figL = px.pie(melted, values= 'values', title='MISSED', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'DUE': 'red', 'BLED': 'green'} )

cola, colb, colc = st.columns(3)
with cola:
    st.plotly_chart(figL, use_container_width=True)
with colb:
    st.plotly_chart(figY, use_container_width=True)
with colc:
    st.plotly_chart(fig6, use_container_width=True)
