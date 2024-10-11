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
<table style="width:100%">
  <tr>
    <th >EMR COLUMN</th>
    <th>RENAME TO:</th> 
    <th>EMR COLUMN</th>
    <th>RENAME TO:</th>
  </tr>
 <tr>
    <td><b>1. HIV Clinic No.</b></td>
    <td><b>ART</b></td>
    <td><b>2. ART START DATE</b></td>
     <td><b>AS</b></td>
 </tr>
 <tr>
    <td><b>3. TRANSFER OUT DATE</b></td>
    <td><b>TO</b></td>
    <td><b>4. Death Date</b></td>
     <td><b>DD</b></td>
 </tr>
  <tr>
    <td><b>5. LAST ENCOUNTER DATE</b></td>
    <td><b>LD</b></td>
    <td><b>6. FIRST ENCOUNTER DATE</b></td>
     <td><b>FE</b></td>
 </tr>
  <tr>
    <td><b>7. RETURN VISIT DATE</b></td>
    <td><b>RD</b></td>
    <td><b>8. RETURN VISIT DATE1</b></td>
     <td><b>RD1</b></td>
 </tr>
  <tr>
    <td><b>9.RETURN VISIT DATE2</b></td>
    <td><b>RD2</b></td>
    <td><b>10.RETURN VISIT DATE_Obs Date</b></td>
     <td><b>RDO</b></td>
 </tr>
  <tr>
    <td><b>11. TRANSFER IN OBS DATE</b></td>
    <td><b>TI</b></td>
    <td><b>12. HIV VIRAL LOAD DATE </b></td>
     <td><b>VD</b></td>
 </tr>
   <tr>
    <td><b>13. ARV REGIMEN DAYS DISPENSED</b></td>
    <td><b>ARVD</b></td>
    <td><b>14. ARV REGIMEN DAYS DISPENSED_obsDatetime</b></td>
     <td><b>ARVDO</b></td>
 </tr>
</table>
"""
# Display the HTML table using markdown in Streamlit
st.markdown(html_table, unsafe_allow_html=True)
