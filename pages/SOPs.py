import pandas as pd 
import streamlit as st 
from datetime import datetime

st.set_page_config(
    page_title = 'SOPs',
    page_icon =":bar_chart"
    )

#st.header('CODE UNDER MAINTENANCE, TRY AGAIN TOMORROW')
#st.stop()
cola,colb,colc = st.columns([1,3,1])
colb.subheader('SOPs FOR PROGRAM GROWTH')

today = datetime.now()
todayd = today.strftime("%Y-%m-%d")# %H:%M")
wk = today.strftime("%V")
week = int(wk)-39
cola,colb = st.columns(2)
cola.write(f"**DATE TODAY:    {todayd}**")
colb.write(f"**CURRENT WEEK:    {week}**")

# HTML Table
html_table = """
<table>
  <tr>
    <th>Purpose: To harmonize the procedure of extraction of patient lists from UgandaEMR using Cohort builder </th>
  </tr>
</table>
"""
# Display the HTML table using markdown in Streamlit
st.markdown(html_table, unsafe_allow_html=True)

# HTML Table
html_table = """
<p> 
Run ever-enrolled list with HIV Clinic no, Gender, Age, Telephone Number, Last Encounter date, First encounter date, Return visit date (check location, check obs datetime, return most recent 3 RVDs), Transferred out to another facility, Transfer In, Current ARV regimen, ART START date, Deceased, ART days dispensed (check obs datetime)
</p>
<p>-Filter HIV Clinic No to remove blanks and maintain PLHIV only. (those with a patient ID)</p>
"""
# Display the HTML table using markdown in Streamlit
st.markdown(html_table, unsafe_allow_html=True)
