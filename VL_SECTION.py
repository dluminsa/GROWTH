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
import datetime as dt

# st.set_page_config(
#     page_title = 'VL SECTION',
#     page_icon =":bar_chart"
#     )

#st.header('CODE UNDER MAINTENANCE, TRY AGAIN TOMORROW')
#st.stop()
cola,colb,colc = st.columns([1,3,1])
colb.subheader('VIRAL LOAD COVERAGE')

today = datetime.now()
todayd = today.strftime("%Y-%m-%d")# %H:%M")
wk = today.strftime("%V")
week = int(wk) + 13
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
         st.write("POOR NETWORK, COULDN'T CONNECT TO DATABASE")
         st.stop()
dftx = st.session_state.vl.copy()

if 'line' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'LINELISTS', usecols=list(range(21)),ttl=5)
        df = exist.dropna(how='all')
        st.session_state.line = df
     except exception as e:
         st.write(f'{e}')
         st.write("POOR NETWORK, COULDN'T CONNECT TO DATABASE")
         st.stop()
dfline = st.session_state.line.copy()

if 'summ' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'SUMM', usecols=list(range(16)),ttl=5)
        df = exist.dropna(how='all')
        st.session_state.sum = df
     except exception as e:
         st.write(f'{e}')
         st.write("POOR NETWORK, COULDN'T CONNECT TO DATABASE")
         st.stop()
dfsum = st.session_state.sum.copy()


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
    dfline2 = dfline.copy()
    dfsum2 = dfsum.copy()

else:
    dfrep['CLUSTER'] = dfrep['CLUSTER'].astype(str)
    dfrep2 = dfrep[dfrep['CLUSTER'].isin(CLUSTER)].copy()

    dftx['CLUSTER'] = dftx['CLUSTER'].astype(str)
    dftx2 = dftx[dftx['CLUSTER'].isin(CLUSTER)].copy()
    
    water['CLUSTER'] = water['CLUSTER'].astype(str)
    water2 = water[water['CLUSTER'].isin(CLUSTER)].copy()
     
    dfline['CLUSTER'] = dfline['CLUSTER'].astype(str)
    dfline2 = dfline[dfline['CLUSTER'].isin(CLUSTER)].copy()

    dfsum['CLUSTER'] = dfsum['CLUSTER'].astype(str)
    dfsum2 = dfsum[dfsum['CLUSTER'].isin(CLUSTER)].copy()

district = st.sidebar.multiselect('**CHOOSE A DISTRICT**', dfrep2['DISTRICT'].unique(), key='b')
if not district:
    dfrep3 = dfrep2.copy()
    dfline3 = dfline2.copy()
    dfsum3  = dfsum2.copy()
    dftx3 = dftx2.copy()
    water3 = water2.copy()
else:
    dfrep2['DISTRICT'] = dfrep2['DISTRICT'].astype(str)
    dfrep3 = dfrep2[dfrep2['DISTRICT'].isin(district)].copy()

    dftx2['DISTRICT'] = dftx2['DISTRICT'].astype(str)
    dftx3 = dftx2[dftx2['DISTRICT'].isin(district)].copy()
    
    water2['DISTRICT'] = water2['DISTRICT'].astype(str)
    water3 = water2[water2['DISTRICT'].isin(district)].copy()

    dfline2['DISTRICT'] = dfline2['DISTRICT'].astype(str)
    dfline3 = dfline2[dfline2['DISTRICT'].isin(district)].copy()

    dfsum2['DISTRICT'] = dfsum2['DISTRICT'].astype(str)
    dfsum3 = dfsum2[dfsum2['DISTRICT'].isin(district)].copy()

facility = st.sidebar.multiselect('**CHOOSE A FACILITY**', dfrep3['FACILITY'].unique(), key='c')
if not facility:
    dfrep4 = dfrep3.copy()
    dftx4 = dftx3.copy()
    water4 = water3.copy()
    dfline4 = dfline3.copy()
    dfsum4 = dfsum3.copy()
else:
    dfrep4 = dfrep3[dfrep3['FACILITY'].isin(facility)].copy()
    dftx4 = dftx3[dftx3['FACILITY'].isin(facility)].copy()
    water4 = water3[water3['FACILITY'].isin(facility)].copy()
    dfline4 = dfline3[dfline3['FACILITY'].isin(facility)].copy()
    dfsum4 = dfsum3[dfsum3['FACILITY'].isin(facility)].copy()


# Base DataFrame to filter
dfrep = dfrep4.copy()
dftx = dftx4.copy()
water = water4.copy()
dfline = dfline4.copy()
dfsum = dfsum4.copy()

# Apply filters based on selected criteria
if CLUSTER:
    dfrep = dfrep[dfrep['CLUSTER'].isin(CLUSTER)].copy()
    dftx = dftx[dftx['CLUSTER'].isin(CLUSTER)].copy()
    dfline = dfline[dfline['CLUSTER'].isin(CLUSTER)].copy()
    dfsum = dfsum[dfsum['CLUSTER'].isin(CLUSTER)].copy()

if district:
    dfrep = dfrep[dfrep['DISTRICT'].isin(district)].copy()
    dftx = dftx[dftx['DISTRICT'].isin(district)].copy()
    dfsum = dfsum[dfsum['DISTRICT'].isin(district)].copy()
    dfline = dfline[dfline['DISTRICT'].isin(district)].copy()
     
if facility:
    dfrep = dfrep[dfrep['FACILITY'].isin(facility)].copy()
    dftx = dftx[dftx['FACILITY'].isin(facility)].copy()
    dfsum = dfsum[dfsum['FACILITY'].isin(facility)].copy()
    dfline = dfline[dfline['FACILITY'].isin(facility)].copy()

dati = dt.date.today()
wiki = dati.strftime('%v')
today = dati.strftime('%d')
mon = dati.strftime('%m')

#keep one entry for summaries
dfsum['FACILITY'] = dfsum['FACILITY'].astype(str)
dfsum['WEEK'] = pd.to_numeric(dfsum['WEEK'], errors = 'coerce')
dfsum = dfsum.sort_values(by = ['WEEK'])
dsfum = dfsum.drop_duplicates(subset = 'FACILITY', keep='last')


st.divider()
##TPT SECTION
tpt = dfline[['CLUSTER', 'DISTRICT', 'FACILITY', 'A', 'AS', 'RD', 'Rmonth', 'Rday', 'TPT' ,'TPT STATUS', 'RWEEK']].copy()
tpt= tpt[tpt['TPT STATUS'].notna()].copy()
tpt['TPT STATUS'] = tpt['TPT STATUS'].astype(str)
tptsum = dfsum[['CLUSTER', 'DISTRICT', 'FACILITY','JANTPT', 'FEBTPT','MARTPT', 'WEEK']].copy()
tptsum = tptsum[tptsum['WEEK']==wiki].copy()
tpt['TPT STATUS'] = tpt['TPT STATUS'].astype(str)

loop = df['DISTRICT'].unique()
if len(loop) ==1:
     tpt['USE'] = tpt['FACILITY']
     word = 'FACILITY'
else:
     tpt['USE'] = tpt['DISTRICT']
     word = 'DISTRICT'
cola, colb, colc, cold, cole, colf = st.columns([2,1,1,1,1,1])
cola.write(f'**{word}**')
colb.write('**TODAY**')
colc.write('**THIS WEEK**')
cold.write('**JAN**')
cole.write('**FEB**')
colf.write('**MAR**')

facilities = tpt['USE'].unique()
#SUMMARIES
for fac in facilities:
     tpt = tpt[tpt['USE'] == fac]
     tpt[['Rmonth', 'Rday', 'RWEEK']] = tpt[['Rmonth', 'Rday','RWEEK']].apply(pd.to_numeric, errors='coerce')
     tod = tpt[((tpt['Rmonth'] == mon) & (tpt['Rday'] == today))].copy()
     tods = tod.shape[0]
     wik = tpt[(tpt['RWEEK'] == wiki)].copy()
     wikis = wik.shape[0]
     tpsum = dfsum[dfsum['FACILITY']==fac].copy()
     try:
       jansum = tptsum['JANTPT'].sum()
     except:
          jansum = 0
     try:
          febsum = tptsum['FETPT'].sum()
     except:
          febsum = 0
     try:
          marsum = tptsum['MARTPT'].sum()
     except:
          marsum = 0
          
     cola.write(f'**{fac}**')
     colb.write(f'**{tods}**')
     colc.write(f'**{wikis}**')
     cold.write(f'**{jansum}**')
     cole.write(f'**febsum**')
     colf.wite(f'**{marsum}**')
     
st.write(tpt.shape[0])
st.divider()
#VL COVERAGE

HAVE = water['HAVE'].sum()
NOT = water['NOVL'].sum()
TOTAL = int(HAVE) + int(NOT)
HAVE = int(HAVE)
NOT = int(NOT)
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

# Display the plot
st.write('')
st.write('')
st.write('')
st.success('**CREATED BY Dr. LUMINSA DESIRE**')
