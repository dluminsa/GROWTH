import pandas as pd 
import streamlit as st 
import os
import gspread
from pathlib import Path
import random
import plotly.express as px
import plotly.graph_objects as go
import traceback
import time
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(
    page_title = 'TXML CAMPAIGN',
    page_icon =":bar_chart"
    )

#st.header('CODE UNDER MAINTENANCE, TRY AGAIN TOMORROW')
#st.stop()
cola,colb,colc = st.columns([1,3,1])
colb.subheader('PROGRAM GROWTH')

today = datetime.now()
todayd = today.strftime("%Y-%m-%d")# %H:%M")
wk = today.strftime("%V")
week = int(wk)+13
cola,colb = st.columns(2)
cola.write(f"**DATE TODAY:    {todayd}**")
colb.write(f"**CURRENT WEEK:    {week}**")
dd = int(week)
k = int(wk)
#st.warning('***CURRENT DATA IS FOR DEMONSTRATION ONLY, WILL BE REMOVED AFTER ROLLING OUT THE DASHBOARD**')

if 'tx' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'TX', usecols=list(range(22)),ttl=5)
        tx = exist.dropna(how='all')
        st.session_state.tx = tx
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dftx = st.session_state.tx.copy()
# #st.write(dftx)

if 'q4' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'Q4', usecols=list(range(24)),ttl=5)
        tx = exist.dropna(how='all')
        st.session_state.erl = tx 
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dfearly = st.session_state.erl.copy()



#REPORTING RATES
@st.cache_data
def report():
    df = pd.read_csv('CLUSTERS.csv')
    df['Q1'] = pd.to_numeric(df['Q1'], errors='coerce')
    df = df[df['Q1']>0].copy()
    return df  

dfrep = report()
dfa = dfrep[['DISTRICT', 'FACILITY']].copy() ## EXPECTED DISTRICTS
dftx['SURGE'] = pd.to_numeric(dftx['SURGE'], errors='coerce')
dfb = dftx[dftx['SURGE'] == dd].copy()  #FACILITIES FROM TX SHEET
dfb = dfb[['DISTRICT' , 'FACILITY']]
dfb = dfb.drop_duplicates(subset='FACILITY', keep='last')
dfa['FACILITY'] = dfa['FACILITY'].astype(str)
dfb['FACILITY'] = dfb['FACILITY'].astype(str)
none = dfa[~dfa['FACILITY'].isin(dfb['FACILITY'])].copy()

all = none.shape[0]
buk = none[none['DISTRICT']=='BUKOMANSIMBI'].copy()
semb = none[none['DISTRICT']=='SEMBABULE'].copy()
dist = none[none['DISTRICT']=='MASAKA DISTRICT'].copy()
kal = none[none['DISTRICT']=='KALUNGU'].copy()
city = none[none['DISTRICT']=='MASAKA CITY'].copy()
lwe = none[none['DISTRICT']=='LWENGO'].copy()
lya = none[none['DISTRICT']=='LYANTONDE'].copy()
kala = none[none['DISTRICT']=='KALANGALA'].copy()
mpi = none[none['DISTRICT']=='MPIGI'].copy()
goa = none[none['DISTRICT']=='GOMBA'].copy()
but = none[none['DISTRICT']=='BUTAMBALA'].copy()
wak = none[none['DISTRICT']=='WAKISO'].copy()
rak = none[none['DISTRICT']=='RAKAI'].copy()
kyo = none[none['DISTRICT']=='KYOTERA'].copy()


bu = buk.shape[0]
se = semb.shape[0]
di = dist.shape[0]
ka = kal.shape[0]
ci = city.shape[0]
ky = kyo.shape[0]
rk = rak.shape[0]
waki = wak.shape[0]
bt = but.shape[0]
g =  goa.shape[0]
mp = mpi.shape[0]
kal = kala.shape[0]
ly = lya.shape[0]
lw = lwe.shape[0]


if kal ==0: ####KALAGALA
   kg = 'all facilities have reported'
else:
   kg = f'{kal}'

if waki ==0: ####WAKISO
   wak = 'all facilities have reported'
else:
   wak = f'{waki}'

if mp ==0: ####MPIGI
   mpi = 'all facilities have reported'
else:
   mpi = f'{mp}'

if g ==0: ####GOMBA
   gom = 'all facilities have reported'
else:
   gom = f'{g}'

if bt ==0: ####BUTAMBALA
   but = 'all facilities have reported'
else:
   but = f'{bt}'


if lw ==0: ####LWENGO
   lwe = 'all facilities have reported'
else:
   lwe = f'{lw}'

if ly ==0: ####LYANTONDE
    lya= 'all facilities have reported'
else:
   lya = f'{ly}'


if rk ==0: ####RAKAI
   r = 'all facilities have reported'
else:
   r = f'{rk}'

if ky ==0: ####KYOTERA
   y = 'all facilities have reported'
else:
   y = f'{ky}'
 
if bu ==0:
   b = 'all facilities have reported'
else:
   b = f'{bu}'
    
if se ==0:
   s = 'all facilities reported'
else:
   s = f'{se}'
    
if di ==0:
   d = 'all facilities reported'
else:
   d = f'{di}'
    
if ka ==0:
   k = 'all facilities reported'
else:
   k = f'{ka}'
    
if ci ==0:
   c = 'all facilities reported'
else:
   c = f'{ci}'
if all ==0:
    st.write('** ALL FACILITIES HAVE REPORTED**')
else:
    st.divider()
    st.markdown(f"**{all} FACILITIES HAVEN'T REPORTED THIS WEEK**")
    st.markdown(f'**KALANGALA {kg}, WAKISO {wak}, BUKOMANSIMBI {b}, SEMBABULE {s}, KALUNGU {k}, MKA CITY {c}, MKA DISTRICT {d}, MPIGI {mpi}, BUTAMBALA {but}, GOMBA {gom},LYANTONDE {lya}, LWENGO {lwe}, KYOTERA {y}, RAKAI {r}**')
    with st.expander('ClICK TO SEE PENDING FACILITIES'):
        cola, colb = st.columns(2)
        none = none.reset_index()
        none = none.drop(columns='index')
        disty = none['DISTRICT'].unique()
        dyu = colb.selectbox('FILTER BY DISTRICT', disty, index=None)
        none['DISTRICT'] = none['DISTRICT'].astype(str)
        if not dyu:
             nonedis = none.copy()
        else:
             nonedis = none[none['DISTRICT'] == dyu].copy()
             nonedis = nonedis.reset_index()
             nonedis = nonedis.drop(columns='index')
       
        st.dataframe(nonedis)
#######################FILTERS
clusters = dfrep['CLUSTER'].unique()


fac = dfearly['FACILITY'].unique()

#TO USE WHERE WEEKS WE DON'T NEED TRENDS
dfy = []
for every in fac:
    dff = dfearly[dfearly['FACILITY']== every]
    dff = dff.drop_duplicates(subset=['FACILITY'], keep = 'last')
    dfy.append(dff)
water = pd.concat(dfy)



#REMOVE DUPLICATES FROM EARLY SHEET # HOLD THIS IN SESSION LATER
dfearly['DATEX'] = pd.to_datetime(dfearly['DATE'], errors='coerce')
dfearly['DAY'] = dfearly['DATEX'].dt.day
dfearly['DAY'] = pd.to_numeric(dfearly['DAY'], errors='coerce')
days = dfearly['DAY'].unique()
dfs=[]   
for each in days:
    dfearly['DAY'] = pd.to_numeric(dfearly['DAY'], errors='coerce')
    dfa = dfearly[dfearly['DAYS']==each]
    dfa = dfa.drop_duplicates(subset=['FACILITY'], keep = 'last')
    dfs.append(dfa)
dfearly = pd.concat(dfs)

#FILTERS
st.sidebar.subheader('**Filter from here**')
CLUSTER = st.sidebar.multiselect('CHOOSE A CLUSTER', clusters, key='a')

#create for the state
if not CLUSTER:
    dfearly2 = dfearly.copy()
    dfrep2 = dfrep.copy()
    water2 = water.copy()

else:
   
    dfearly['CLUSTER'] = dfearly['CLUSTER'].astype(str)
    dfearly2 = dfearly[dfearly['CLUSTER'].isin(CLUSTER)]

    dfrep['CLUSTER'] = dfrep['CLUSTER'].astype(str)
    dfrep2 = dfrep[dfrep['CLUSTER'].isin(CLUSTER)]
    
    water['CLUSTER'] = water['CLUSTER'].astype(str)
    water2 = water[water['CLUSTER'].isin(CLUSTER)]

district = st.sidebar.multiselect('**CHOOSE A DISTRICT**', dfrep2['DISTRICT'].unique(), key='b')
if not district:
    dfearly3 = dfearly2.copy()
    dfrep3 = dfrep2.copy()
    water3 = water2.copy()
else:
    dfearly2['DISTRICT'] = dfearly2['DISTRICT'].astype(str)
    dfearly3 = dfearly2[dfearly2['DISTRICT'].isin(district)].copy()

    dfrep2['DISTRICT'] = dfrep2['DISTRICT'].astype(str)
    dfrep3 = dfrep2[dfrep2['DISTRICT'].isin(district)].copy()
    
    water2['DISTRICT'] = water2['DISTRICT'].astype(str)
    water3 = water2[water2['DISTRICT'].isin(district)].copy()

facility = st.sidebar.multiselect('**CHOOSE A FACILITY**', dfrep3['FACILITY'].unique(), key='c')
if not facility:
    dfearly4 = dfearly3.copy()
    dfrep4 = dfrep3.copy()
    water4 = water3.copy()
else:
    dfearly4 = dfearly3[dfearly3['FACILITY'].isin(facility)].copy()
    dfrep4 = dfrep3[dfrep3['FACILITY'].isin(facility)].copy()
    water4 = water3[water3['FACILITY'].isin(facility)].copy()

# Base DataFrame to filter

dfearly = dfearly4.copy()
dfrep = dfrep4.copy()
water = water4.copy()


# Apply filters based on selected criteria
if CLUSTER:
    water = water[water['CLUSTER'].isin(CLUSTER)].copy()
    dfearly = dfearly[dfearly['CLUSTER'].isin(CLUSTER)].copy()
    dfrep = dfrep[dfrep['CLUSTER'].isin(CLUSTER)].copy()

if district:
    water = water[water['DISTRICT'].isin(district)].copy()
    dfearly = dfearly[dfearly['DISTRICT'].isin(district)].copy()
    dfrep = dfrep[dfrep['DISTRICT'].isin(district)].copy()
  

if facility:
    water = water[water['FACILITY'].isin(facility)].copy()
    dfearly = dfearly[dfearly['FACILITY'].isin(facility)].copy()
    dfrep = dfrep[dfrep['FACILITY'].isin(facility)].copy()
st.write(water)    
check = water.shape[0]
if check == 0:
    st.warning('***NO DATA FOR THE SELECTION MADE**')
    st.stop()
else:
    pass

st.divider()
cola, colb, colc = st.columns(3)
colb.success('**QUICK SUMMARY**')
cola, colb, colc = st.columns(3)
cola.info('**Q1 CURR**')
colb.info('**Q2 CURR**')
colc.info('**BALANCE**')

q1 = dfearly['Q1'].sum()
q2 = dfearly['Q2'].sum()
bal  = q1-q2
q1 = int(q1)
q2 = int(q2)
bal = int(bal)
if bal == 0:
    bal = 'ACHIEVED'
elif bal <0:
    bal = 'EXCEEDED'
else:
    pass


cola.metric(label='a', value =f'{q1}', label_visibility='hidden')
colb.metric(label='b', value =f'{q2}', label_visibility='hidden')
colc.metric(label='c', value =f'{bal}', label_visibility='hidden')

st.write('**WEEKLY TREND LINE SHOWING INCREASE IN TXCURRs, VL COVERAGE AND REDUCTION IN TXML**')

grouped = dfearly.groupby('DAY').sum(numeric_only=True).reset_index()

melted = grouped.melt(id_vars=['DAY'], value_vars=['Q1', 'Q2', 'LOST'],
                            var_name='INTERVAL', value_name='Total')
fig2 = px.line(melted, x='DAY', y='Total', color='INTERVAL', markers=True,
              title='DAILY TRENDS IN TXCURR, TXML AND VL', labels={'DAY':'DAYS', 'Total': 'No. of clients', 'INTERVAL': 'VARIABLES'})
fig2.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)
fig2.update_xaxes(type='category')
st.plotly_chart(fig2, use_container_width= True)
st.write("**FACILITIES THAT HAVE EXCEEDED Q1 CURRS**")
dfearly['CHECK'] = dfearly['Q2']- dfearly['Q1']
exceeded = dfearly[dfearly['CHECK']>0]
st.write("")
st.write("")
st.write("")
st.write("**FACILITIES THAT HAVE ACHIEVED Q1 CURRS**")
achieved = dfearly[dfearly['CHECK']==0]
st.write("")
st.write("")
st.write("")
st.write("**FACILITIES THAT HAVE DROPPED TX CURRS**")
exceeded = dfearly[dfearly['CHECK']>0]               
st.stop()














wik = week -2 
st.write(f'**APPOINTMENTS SINCE 3rd SEPT TO WEEK {wik}**')

mostd = water.groupby('DISTRICT')['TWO'].sum()
mostf = water.groupby('FACILITY')['TWO'].sum()

####TOP3
topdis3 = mostd.nlargest(3)
topdis3 = topdis3.reset_index()
mostdis3 = ','.join(topdis3['DISTRICT'].unique())

topfas3 = mostf.nlargest(3)
topfas3 = topfas3.reset_index()
mostfas3 = ','.join(topfas3['FACILITY'].unique())

##TOP 2
topdis2 = mostd.nlargest(2)
topdis2 = topdis2.reset_index()
mostdis2 = ','.join(topdis2['DISTRICT'].unique())


checkf = water['FACILITY'].nunique()
checkd = water['DISTRICT'].nunique()
if facility and not CLUSTER and not district:
    pass
elif checkf <3:
    pass
elif checkd >3:
    st.success(f'**MOST AFFECTED DISTRICS ARE {mostdis3}, MOST AFFECTED FACILITIES ARE {mostfas3}**')
elif checkd ==2:
    st.success(f'**MOST AFFECTED DISTRICS ARE {mostdis2}, MOST AFFECTED FACILITIES ARE {mostfas3}**')
elif checkd ==1:
    st.success(f'**MOST AFFECTED FACILITIES ARE {mostfas3}**')

        
st.divider()
#############################################################################################
#filtered_df = filtered_df[filtered_df['WEEK']==k].copy()
pote = water['POTENTIAL'].sum()
Q4 = water['Q4'].sum()
ti = water['TI'].sum()
new = water['TXNEW'].sum()
rt = water['RTT'].sum()  
pot = int(Q4)+int(ti)+int(new) + int(rt)
los = water['TWO'].sum()
to  = water['TO'].sum()
dd = water['DEAD'].sum()
Q1 = water['ACTIVE'].sum()
#uk = int(pot) - int(ti)- int(Q4) - int(new)
uk = int(pote) - int(pot) 

labels = ["Q4 Curr",   "TI",     "TX NEW",     'RTT' ,  "Potential",  "MISSED",  "DEAD",     "TO",   "Unknown",  "ACTIVE"]
values = [Q4,           ti,        new,         rt,       pot,        -los,       -dd,        -to,     uk,          Q1]
measure = ["absolute", "relative","relative", "relative","total",    "relative", "relative","realative","realative","total"]
# Create the waterfall chart

fig = go.Figure(go.Waterfall(
    name="Waterfall",
    orientation="v",
    measure=measure,
    x=labels,
    textposition="outside",
    text=[f"{v}" for v in values],
    y=values
))

# Add titles and labels and adjust layout properties
fig.update_layout(
    title="Waterfall Analysis",
    xaxis_title="Categories",
    yaxis_title="Values",
    showlegend=True,
    height=425,  # Adjust height to ensure the chart fits well
    margin=dict(l=20, r=20, t=60, b=20),  # Adjust margins to prevent clipping
    yaxis=dict(automargin=True)
)

# Show the plot
st.plotly_chart(fig)
#####################ONLY SHOWS WHEN THERE ARE MANY FACILITIES OR DISTRTICTS
dist = water['DISTRICT'].nunique()
fact = water['FACILITY'].nunique()


if int(dist) > 1:
    st.divider()
    x = []
    y = []
    water['TWO'] = pd.to_numeric(water['TWO'], errors='coerce')
    districts = water['DISTRICT'].unique()
    water = water.sort_values(by = ['TWO'], ascending = False)
    for each in districts:
        x.append(each)
        dist = water[water['DISTRICT']==each]['TWO'].sum()
        y.append(dist)   
 
    sorted_indices = sorted(range(len(y)), key=lambda i: y[i], reverse=True)
    x = [x[i] for i in sorted_indices]
    y = [y[i] for i in sorted_indices]
    num_bars = len(x)
    colors = [f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)' for _ in range(num_bars)]
    
    figd = go.Figure(data=[
        go.Bar(x=x, y=y, marker_color=colors)
    ])
    
    # Update layout
    figd.update_layout(
        title='TOTAL MISSED APPOINTMENTS SINCE THE QUARTER BEGAN PER DISTRICT',
        xaxis_title='District',
        yaxis_title='TOTAL MISSED APPOINTMENTS',
        xaxis_tickangle=-45  # Optional: angle x-axis labels for better visibility
    )
    st.plotly_chart(figd)#, use_container_width=True)
elif int(fact) > 1:
    st.divider()
    x = []
    y = []
    water['TWO'] = pd.to_numeric(water['TWO'], errors='coerce')
    districts = water['FACILITY'].unique()
    water = water.sort_values(by = ['TWO'], ascending = False)
    for each in districts:
        x.append(each)
        dist = water[water['FACILITY']==each]['TWO'].sum()
        y.append(dist)   
 
    sorted_indices = sorted(range(len(y)), key=lambda i: y[i], reverse=True)
    x = [x[i] for i in sorted_indices]
    y = [y[i] for i in sorted_indices]
    num_bars = len(x)
    colors = [f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)' for _ in range(num_bars)]
    
    figd = go.Figure(data=[
        go.Bar(x=x, y=y, marker_color=colors)
    ])
    
    # Update layout
    distict = '.'.join(water['DISTRICT'].unique())
    figd.update_layout(
        title=f'TOTAL MISSED APPOINTMENTS SINCE THE QUARTER BEGAN PER FACILITY IN {distict} DISTRICT',
        xaxis_title='FACILITIES',
        yaxis_title='TOTAL MISSED APPOINTMENTS',
        xaxis_tickangle=-45  # Optional: angle x-axis labels for better visibility
    )
    st.plotly_chart(figd)#, use_container_width=True)
    
else:
    pass    

#############################################################################################
#LINE GRAPHS
st.divider()
#TREND OF MISSED APOINTMENTS
st.success('**TRENDS IN CLIENTS WHO HAVE MISSED APPOINTMENTS FOR MORE THAN 2, 3 AND 4 WEEKS**')

grouped = dftx.groupby('SURGE').sum(numeric_only=True).reset_index()

melted = grouped.melt(id_vars=['SURGE'], value_vars=['TWO', 'THREE', 'FOUR'],
                            var_name='INTERVAL', value_name='Total')
fig2 = px.line(melted, x='SURGE', y='Total', color='INTERVAL', markers=True,
              title='MISSED APPOINTMENTS FOR MORE THAN 2, 3 OR 4 WEEKS', labels={'SURGE':'WEEK', 'Total': 'No. of clients', 'INTERVAL': 'VARIABLES'})

# melted = grouped.melt(id_vars=['SURGE'], value_vars=['TWO', 'THREE', 'FOUR'],
#                             var_name='INTERVAL', value_name='Total')

melted2 = grouped.melt(id_vars=['SURGE'], value_vars=['RTT', 'TO','DEAD'],
                            var_name='INTERVAL', value_name='Total')
melted['SURGE'] = melted['SURGE'].astype(int)
melted['SURGE'] = melted['SURGE'].astype(str)
melted2['SURGE'] = melted2['SURGE'].astype(int)
melted2['SURGE'] = melted2['SURGE'].astype(str)

fig2 = px.line(melted, x='SURGE', y='Total', color='INTERVAL', markers=True,
              title='MISSED APPOINTMENTS FOR MORE THAN 2, 3 OR 4 WEEKS', labels={'SURGE':'WEEK', 'Total': 'No. of clients', 'INTERVAL': 'VARIABLES'})

fig3 = px.line(melted2, x='SURGE', y='Total', color='INTERVAL', markers=True, color_discrete_sequence=['black','red', 'yellow'],
              title='RTT VS TO VS DEAD', labels={'SURGE':'WEEK', 'Total': 'No. of clients', 'INTERVALS': 'VARIABLES'})

fig2.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)
fig2.update_xaxes(type='category')
st.plotly_chart(fig2, use_container_width= True)
fig3.update_layout(
    width=800,  # Set the width of the plot
    height = 400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)
fig3.update_xaxes(type='category')
colx,coly = st.columns([2,1])
with colx:
    st.plotly_chart(fig2, use_container_width= True)

with coly:
    st.plotly_chart(fig3, use_container_width= True)
    #st.plotly_chart(fig3, use_container_width=True)
#############################################################################################
# #HIGHEST TXML 
st.divider()
highest = water[water['TWO']>299]

highest = highest.sort_values(by=['TWO'])#, ascending=False)
highesta = highest.shape[0]

highesty = water[water['TWO']<300]
highesty = highesty[highesty['TWO']>199]
highestb = highesty.sort_values(by=['TWO'], ascending=False)
highestb = highestb.shape[0]
# highestb = highest[highest['WEEK']==m]

coly, colu = st.columns(2)
with coly:
    if highesta ==0:
        st.warning('**FACILITY SELECTED IS NOT AMONG**')
        pass
    else:
        figa = px.bar(
        highest,
        x='TWO',
        y='FACILITY',
        orientation='h',
        title='FACILITIES WITH >300 MISSED APPTS',
        labels={'TWO': 'CLIENTS MISSED', 'FACILITY': 'Facility'}
            )
        figa.update_traces(marker_color='#be7869')
        st.plotly_chart(figa, use_container_width=True)
with colu:
    if highestb ==0:
        st.write('**FACILITY SELECTED IS NOT AMONG**')
        pass
    else:
        figa = px.bar(
        highesty,
        x='TWO',
        y='FACILITY',
        orientation='h',
        title='FACILITIES WITH 200-300 MISSED APPTS',
        labels={'TWO': 'CLIENTS MISSED', 'FACILITY': 'Facility'}
        )
        figa.update_traces(marker_color='green')
        st.plotly_chart(figa, use_container_width=True)
st.divider()
st.divider()
highest = water[water['TWO']>99].copy()
highest = highest[highest['TWO']<200]

highest = highest.sort_values(by=['TWO'])#, ascending=False)
highesta = highest.shape[0]

highesty = water[water['TWO']<100]
highesty = highesty[highesty['TWO']>49]
highestb = highesty.sort_values(by=['TWO'], ascending=False)
highestb = highestb.shape[0]
# highestb = highest[highest['WEEK']==m]

coly, colu = st.columns(2)
with coly:
    if highesta ==0:
        st.warning('**FACILITY SELECTED IS NOT AMONG**')
        pass
    else:
        figa = px.bar(
        highest,
        x='TWO',
        y='FACILITY',
        orientation='h',
        title='FACILITIES WITH 100-200 MISSED APPTS',
        labels={'TWO': 'CLIENTS MISSED', 'FACILITY': 'Facility'}
            )
        figa.update_traces(marker_color='#be7869')
        st.plotly_chart(figa, use_container_width=True)
with colu:
    if highestb ==0:
        st.write('**FACILITY SELECTED IS NOT AMONG**')
        pass
    else:
        figa = px.bar(
        highesty,
        x='TWO',
        y='FACILITY',
        orientation='h',
        title='FACILITIES WITH 50-100 MISSED APPTS',
        labels={'TWO': 'CLIENTS MISSED', 'FACILITY': 'Facility'}
        )
        figa.update_traces(marker_color='green')
        st.plotly_chart(figa, use_container_width=True)
st.divider()
#MMD PERFORMANCE
#OF THOSE THAT ARE DUE, HOW MANY ARE OURS, HOW MANY ARE VISITOR

dftx[['M2','M3', 'M6']] = dftx[['M2','M3', 'M6']].apply(pd.to_numeric, errors='coerce')
M2 = water['M2'].sum()
M3 = water['M3'].sum()
M6 = water['M6'].sum()


# Creating the grouped bar chart
fig4 = go.Figure(data=[
    go.Bar(name='<3 MTHS', x=['<3 MTHS'], y=[M2], marker=dict(color='red')),
    go.Bar(name='3-5 MTHS', x=['3-5 MTHS'], y=[M3], marker=dict(color='green')),
    go.Bar(name='6+ MTHS', x=['6+ MTHS'], y=[M6], marker=dict(color='blue'))
])

# Setting the layout to have no gap between bars
fig4.update_layout(barmode='group', bargap=0, bargroupgap=0)

NO_MMD = M2
MMD = int(M3) + int(M6)

labels = ['NO MMD', 'MMD']
values = [NO_MMD, MMD]
# Specify custom colors
colors = ['DarkRed', 'purple']  # Colors for NO_MMD and MMD
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

M2 = int(M2)
M3 = int(M3)
M6 = int(M6)
# Display the chart
st.success(f'**{M2} Clients were given < 3 Months, {M3} received between 4 to 5 five months, {M6} received 6+ MTHS**')
cola,colb = st.columns(2)
with cola:
    st.plotly_chart(fig4, use_container_width=True)

with colb:
    st.markdown('')
    st.markdown('')
    st.plotly_chart(figp, use_container_width=True)

st.divider()
##########################################################################
#######ONE YEAR COHORT
#filtered_df = filtered_df[filtered_df['WEEK']==k].copy()

total = wateryr['TOTAL'].sum()
newti = wateryr['TI'].sum()
newlydx = wateryr['ORIG'].sum()

newlos = wateryr['LOST'].sum()
newto  = wateryr['TO'].sum()
newdd = wateryr['DEAD'].sum()
active = wateryr['ACTIVE'].sum()

labels = ["NEWLY DX", "TIs", "TOTAL", 'LTFU',"TOs","DEAD", "ACTIVE"]
values = [newlydx, newti, total, -newlos, -newto,-newdd, active]
measure = ["absolute", "relative", "total", "relative", "relative", "relative","total"]
# Create the waterfall chart
figy = go.Figure(go.Waterfall(
    name="Waterfall",
    orientation="v",
    measure=measure,
    x=labels,
    textposition="outside",
    text=[f"{v}" for v in values],
    y=values
))

# Add titles and labels and adjust layout properties
figy.update_layout(
    title="ONE YEAR COHORT ANALYSIS",
    xaxis_title="Categories",
    yaxis_title="Values",
    showlegend=True,
    height=425,  # Adjust height to ensure the chart fits well
    margin=dict(l=20, r=20, t=60, b=20),  # Adjust margins to prevent clipping
    yaxis=dict(automargin=True)
)

st.plotly_chart(figy)
st.divider()
########################################################################################
#ONE YEAR PIE CHART
col1, col2 = st.columns(2)
pied = wateryr.copy()#[filtered_df['WEEK']==k]
#pied['LOST NEW'] = pied['ORIGINAL COHORT']- pied['ONE YEAR ACTIVE'] 
pied = pied[['LOST', 'ACTIVE']]
melted = pied.melt(var_name='Category', value_name='values')
fig = px.pie(melted, values= 'values', title='ONE YEAR RETENTION RATE', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'LOST': 'red', 'ACTIVE': 'blue'} )
    #fig.update_traces(text = 'RETENTION', text_position='Outside')
grouped = dfyr.groupby('SURGE').sum(numeric_only=True).reset_index()

melted = grouped.melt(id_vars=['SURGE'], value_vars=['ACTIVE', 'LOST'],
                            var_name='OUTCOME', value_name='Total')
melted['SURGE'] = melted['SURGE'].astype(int)
melted['SURGE'] = melted['SURGE'].astype(str)
colors = ['DarkRed', 'purple']


fig2 = px.line(melted, x='SURGE', y='Total', color='OUTCOME', markers=True,
              title='MISSED APPOINTMENTS FOR 1 YR', labels={'SURGE':'WEEK', 'Total': 'No. of clients', 'OUTCOME': 'OUTCOME'})

fig2.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
    #marker=dict(colors=colors)
)


fig2.update_xaxes(type='category')
if pied.shape[0]==0:
    pass
else:
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

###############################
st.divider()
st.info('**EARLY RETENTION**')
st.write('**NOTE: The 9 months cohort will be the focus for 1 year cohort next quarter, the TX NEWs are the clients diagnosed this quarter**') 
pied = wateryr.copy()#[filtered_df['WEEK']==k]
#pied['LOST NEW'] = pied['ORIGINAL COHORT']- pied['ONE YEAR ACTIVE'] 
pied = pied[['LOSTS', 'ACTIVES']]
pied = pied.rename(columns={'LOSTS':'LOST', 'ACTIVES':'ACTIVE'})
melted = pied.melt(var_name='Category', value_name='values')
fig6 = px.pie(melted, values= 'values', title='6 MTHS', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'LOST': 'red', 'ACTIVE': 'blue'} )

pied = waterly.copy()#[filtered_df['WEEK']==k]
#pied['LOST NEW'] = pied['ORIGINAL COHORT']- pied['ONE YEAR ACTIVE'] 
pied = pied[['LOSTT', 'ACTIVET']]
pied = pied.rename(columns={'LOSTT':'LOST', 'ACTIVET':'ACTIVE'})
melted = pied.melt(var_name='Category', value_name='values')
fig3 = px.pie(melted, values= 'values', title='3 MTHS', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'LOST': 'red', 'ACTIVE': 'yellow'} )
#pied['LOST NEW'] = pied['ORIGINAL COHORT']- pied['ONE YEAR ACTIVE']
pied = waterly.copy() 
pied = pied[['LOSTO', 'ACTIVEO']]
pied = pied.rename(columns={'LOSTO':'LOST', 'ACTIVEO':'ACTIVE'})
melted = pied.melt(var_name='Category', value_name='values')
fig1 = px.pie(melted, values= 'values', title='TX NEWS', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'LOST': 'red', 'ACTIVE': 'green'} )
pied = wateryr.copy() 
pied = pied[['LOSTN', 'ACTIVEN']]
pied = pied.rename(columns={'LOSTN':'LOST', 'ACTIVEN':'ACTIVE'})
melted = pied.melt(var_name='Category', value_name='values')
fig9 = px.pie(melted, values= 'values', title='9 MTHS', names='Category', hole=0.3,color='Category',  
             color_discrete_map={'LOST': 'red', 'ACTIVE': 'purple'} )

cola, colb, colc,cold = st.columns(4)
with cola:
    st.plotly_chart(fig9, use_container_width=True)
with colb:
    st.plotly_chart(fig6, use_container_width=True)
with colc:
    st.plotly_chart(fig3, use_container_width=True)
with cold:
    st.plotly_chart(fig1, use_container_width=True)
####TRACKING TXML
st.info('**TRENDS IN TXML (FOR CLIENTS THAT WERE REPORTED AS TXML IN Q4 AND Q3 )**')
grouped = dftx.groupby('SURGE').sum(numeric_only=True).reset_index()
Y = ['Q4 TXML', 'Q3 TXML']

grouped_long = grouped.melt(id_vars='SURGE', value_vars=Y, 
                            var_name='Type', value_name='No. of clients')

# Create the line chart
figM = px.line(grouped_long, 
               x='SURGE', 
               y='No. of clients', 
               color='Type', 
               title='CLIENTS NOT RETURNED FROM Q4 AND Q3', 
               labels={'SURGE': 'WEEK', 'No. of clients': 'No. of clients'},
               markers=True)
figM.for_each_trace(
    lambda trace: trace.update(line=dict(color='green')) if trace.name == 'Q4 TXML' else trace.update(line=dict(color='purple'))
)

# # Update layout for better appearance
figM.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)

# Set x-axis to categorical
figM.update_xaxes(type='category')

# Display the plot
st.plotly_chart(figM, use_container_width=True)
st.divider()

html_table = """
<h4><b><u style="color: green;">CYCLE OF INTERUPTION AND RETURN TO ART (CIRA)</u></b></h4>
"""
st.markdown(html_table, unsafe_allow_html=True)

#LOST IN LESS THAN 3 MONTHS
lesl = watercira['L1'].sum() +  watercira['L10'].sum() + watercira['L20'].sum() + watercira['L30'].sum() + watercira['L40'].sum() +  watercira['L50'].sum() + watercira['LG50'].sum()
#LOST IN 3 to 5 MTHS
thrl = watercira['L13'].sum() +  watercira['L103'].sum() + watercira['L203'].sum() + watercira['L303'].sum() + watercira['L403'].sum() +  watercira['L503'].sum() + watercira['LG503'].sum()
#LOST IN 6 MTHS
sixl = watercira['L16'].sum() +  watercira['L106'].sum() + watercira['L206'].sum() + watercira['L306'].sum() + watercira['L406'].sum() +  watercira['L506'].sum() + watercira['LG506'].sum()

#ACTIVE THAN 3 MONTHS
lesA = watercira['A1'].sum() +  watercira['A10'].sum() + watercira['A20'].sum() + watercira['A30'].sum() + watercira['A40'].sum() +  watercira['A50'].sum() + watercira['AG50'].sum()
#ACTIVE IN 3 to 5 MTHS
thrA = watercira['A13'].sum() +  watercira['A103'].sum() + watercira['A203'].sum() + watercira['A303'].sum() + watercira['A403'].sum() +  watercira['A503'].sum() + watercira['AG503'].sum()
#ACTIVE IN 6 MTHS
sixA = watercira['A16'].sum() +  watercira['A106'].sum() + watercira['A206'].sum() + watercira['A306'].sum() + watercira['A406'].sum() +  watercira['A506'].sum() + watercira['AG506'].sum()

totallos = lesl + thrl + sixl
totalact = lesA + thrA + sixA
totalcira = totallos + totalact

# Creating the grouped bar chart
figC = go.Figure(data=[
    go.Bar(name='IIT(TOTAL)', x=['IIT(TOTAL)'], y=[totalcira], marker=dict(color='rgb(0, 71, 171)')),  # Cobalt Blue,
    go.Bar(name='RETURNED', x=['RETURNED'], y=[totalact], marker=dict(color='green'))
])

# Setting the layout to have no gap between bars
figC.update_layout(title = 'Returning clients to ART', barmode='group', bargap=0, bargroupgap=0)


###STACKED BAR CHART
totalact = lesA + thrA + sixA

# Define the values for the variables
a = lesA
b = thrA
c = sixA

#LESS THAN 1 YR
a1 = watercira['A1'].sum() + watercira['A13'].sum() + watercira['A16'].sum()
a2 = a1 + watercira['L1'].sum() + watercira['L13'].sum() + watercira['L16'].sum() 
if a2 ==0:
   a3 = 0
else:
   a3 = round(int((a1/a2)*100))
     
#LESS THAN 10 YRs
a21 = watercira['A10'].sum() + watercira['A103'].sum() + watercira['A106'].sum()
a22 = a21 + watercira['L10'].sum() + watercira['L103'].sum() + watercira['L106'].sum() 
if a22 ==0:
   a23 = 0
else:
   a23 = round(int((a21/a22)*100))

#LESS THAN 20 YRs
a31 = watercira['A20'].sum() + watercira['A203'].sum() + watercira['A206'].sum()
a32 = a31 + watercira['L20'].sum() + watercira['L203'].sum() + watercira['L206'].sum() 
if a32 ==0:
   a33 = 0
else:
   a33 = round(int((a31/a32)*100))

#LESS THAN 30 YRs
a41 = watercira['A30'].sum() + watercira['A303'].sum() + watercira['A306'].sum()
a42 = a41 + watercira['L30'].sum() + watercira['L303'].sum() + watercira['L306'].sum() 
if a42 ==0:
   a43 = 0
else:
   a43 = round(int((a41/a42)*100))

#LESS THAN 40 YRs
a51 = watercira['A40'].sum() + watercira['A403'].sum() + watercira['A406'].sum()
a52 = a51 + watercira['L40'].sum() + watercira['L403'].sum() + watercira['L406'].sum() 
if a52 ==0:
   a53 = 0
else:
   a53 = round(int((a51/a52)*100))
     
#LESS THAN 50 YRs
a61 = watercira['A50'].sum() + watercira['A503'].sum() + watercira['A506'].sum()
a62 = a61 + watercira['L50'].sum() + watercira['L503'].sum() + watercira['L506'].sum() 
if a62 ==0:
   a63 = 0
else:
   a63 = round(int((a61/a62)*100))

#GREATER THAN 50 YRs
a71 = watercira['AG50'].sum() + watercira['AG503'].sum() + watercira['AG506'].sum()
a72 = a71 + watercira['LG50'].sum() + watercira['LG503'].sum() + watercira['LG506'].sum() 
if a72 ==0:
   a73 = 0
else:
   a73 = round(int((a71/a72)*100))

# Create the stacked bar chart
figD = go.Figure()

# Add the bottom layer (a) in cobalt blue
figD.add_trace(go.Bar(
    name='<3 MONTHS',
    y=[a],
    x=['Variables'],
    marker_color='rgb(0, 71, 171)'  # Cobalt blue color
))

# Add the middle layer (b) in green
figD.add_trace(go.Bar(
    name='3-5 MONTHS',
    y=[b],
    x=['Variables'],
    marker_color='green'
))

# Add the top layer (c) in purple
figD.add_trace(go.Bar(
    name='6 + MONTHS',
    y=[c],
    x=['Variables'],
    marker_color='purple'
))

# Update the layout to make it a stacked bar chart
figD.update_layout(
    barmode='stack',
    title='Length of interruption before return',
    yaxis_title='Values'
)
cola, colb,colc, cold = st.columns([1,1,1,3])
cola.write('**AGE**')
colb.write('**Returned**')
colc.write('**IIT(Total)**')
cold.write('**Proportion CIRA Returned**')
cola.write('**<01**')
colb.write(f'**{int(a1)}**')
colc.write(f'**{int(a2)}**')
cold.write(f'**{int(a3)} %**')

cola.write('**1-9**')
colb.write(f'**{int(a21)}**')
colc.write(f'**{int(a22)}**')
cold.write(f'**{int(a23)} %**')

cola.write('**10-19**')
colb.write(f'**{int(a31)}**')
colc.write(f'**{int(a32)}**')
cold.write(f'**{int(a33)} %**')

cola.write('**20-29**')
colb.write(f'**{int(a41)}**')
colc.write(f'**{int(a42)}**')
cold.write(f'**{int(a43)} %**')

cola.write('**30-39**')
colb.write(f'**{int(a51)}**')
colc.write(f'**{int(a52)}**')
cold.write(f'**{int(a53)} %**')

cola.write('**40-49**')
colb.write(f'**{int(a61)}**')
colc.write(f'**{int(a62)}**')
cold.write(f'**{int(a63)} %**')

cola.write('**50+**')
colb.write(f'**{int(a71)}**')
colc.write(f'**{int(a72)}**')
cold.write(f'**{int(a73)} %**')
st.divider()

cola,colb = st.columns(2)
with cola:
    #st.markdown('**Returning clients to ART**')
    st.plotly_chart(figC, use_container_width=True)

with colb:
    #st.markdown('**Length of interruption before return**')
    st.plotly_chart(figD, use_container_width=True)

st.divider()

st.write('')
st.write('')
st.write('')
st.success('**CREATED BY Dr. LUMINSA DESIRE**')



