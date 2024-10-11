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
Run ever-enrolled list with HIV Clinic no, Gender, Age, Telephone Number, Last Encounter date, First encounter date, Return visit date (check location, check obs datetime, return most recent 3 RVDs), Transferred out to another facility, Transfer In, Current ARV regimen, ART START date, Deceased,<i style="background-color: red;"> ART days dispensed (check obs datetime)
</i></p>
"""
# Display the HTML table using markdown in Streamlit
st.markdown(html_table, unsafe_allow_html=True)
st.info('**NOTE THAT ALL THESE STEPS, THE EMR READER WILL DO THEM FOR YOU, THIS IS FOR COMPARISON PURPOSE**')
# HTML Table
html_table = """
<p>Filter HIV Clinic No to remove blanks and maintain PLHIV only. (those with a patient ID)</p>
"""
# Display the HTML table using markdown in Streamlit
st.markdown(html_table, unsafe_allow_html=True)
# HTML Table
html_table = """
<h4>1. APPOINTMENT LIST;</h4>
<p>Using the resultant list,</p>
<ul>
  <li>Remove transfer outs (YES in the TO column)</li>
  <li>Remove deceased (True in the deceased column)</li>
  <li>Then go to the most recent return visit date and select appointment dates of interest.</li>
</ul>
"""
st.markdown(html_table, unsafe_allow_html=True)
html_table = """
<h4>2. MISSED APPOINTMENT LIST;</h4>
<p>Repeat the same steps as for the appointment list after ensuring that the EMR is up to date without any backlog.</p>
<ul>
  <li>In the column of the most recent return visit date, a patient that has a return visit date for the previous period being queried is considered missed.</li>
  <li>For clinics that have community pharmacies using ART access consider locations for ART clinic, Health facility name, and MCH to query missed appointments.</li>
  </ul>
"""
st.markdown(html_table, unsafe_allow_html=True)
# html_table = """
# <h4></h4>
# <p></p>
# <ul>
#   <li></li>
#   <li></li>
#   </ul>
# """
# st.markdown(html_table, unsafe_allow_html=True)

html_table = """
<h4>3. TX-NEW; (Children and adults new on ART in the reporting period)</h4>
<ul>
  <li>Using ever enrolled from UgEMR, go to ART start date and consider the dates for the reporting period say Jan-Mar 24. For O-D 23, consider PLHIV with ART start dates btn O – D 23. </li>
  <li>Exclude transfer-ins as they are being reported by the parent facility.</li>
  </ul>
"""
st.markdown(html_table, unsafe_allow_html=True)
html_table = """
<h4>4. TX-CURR; (Children and adults active on ART in the reporting period)</h4>
<p></p>
<ul>
  <li>From the ever-enrolled extract from UgEMR, remove transfer outs (double check if they are true transfer outs, especially for clients with appointments beyond the reporting period.
	Filter out dead clients (true from the deceased column).
</li>
  <li>Go to the most recent return visit date and select dates from 3rd of the last month of the quarter and beyond which makes the TX-CURR. For example, for Jan-Mar 24, all patients with a return visit date of 3rd March 2024 and beyond should make the TX-CURR list. For O-D 23, consider PLHIV with RVD of 3rd Dec 23 and beyond as TX_CURR. </li>
  <li>Check the current ARV regimen and ensure there are no blanks that may be clients active on pre-ART.</li>
  <li>This includes patients on MMD.</li>
  </ul>
"""
st.markdown(html_table, unsafe_allow_html=True)

html_table = """
<h4>5. TX-ML, (PLHIV active at the start of the reporting period and had no clinical contact since their last expected date).</h4>
<ul>
  <li>From the ever enrolled from UgEMR, filter out patients who were active at the start of the reporting period <b><i style="background-color: red;">and those that initiated ART in the reporting quarter</i></b> but have not returned since their last expected date. Take an example, reporting for Jan-Mar 24, TX-ML list will constitute all patients with a return visit date between 3rd December 2023 to 2nd March 2024. For O-D 23, consider 2nd Sept 23 to 3rd  Dec 2023. </li>
  <li>Leave transfer outs and dead in the ML list.</li>
  </ul>
"""
st.markdown(html_table, unsafe_allow_html=True)

st.markdown(html_table, unsafe_allow_html=True)
html_table = """
<h4>6. TX-RTT, (Patients who returned to care after experiencing an IIT for more than 28 days and remained active until the end of the quarter).</h4>
<p></p>
<ol type='a'>
  <li>From the confirmed TX-CURR list, go to last encounter date and select clients with a last clinical visit in the reporting quarter.</li>
  <li>Go to the column of first encounter date and remove dates for the reporting quarter.</li>
  <li>	Go to ART start date and remove newly enrolled clients on ART in the reporting quarter.</li>
  <li><b><i style="background-color: yellow;">Go to Transfer In and remove transfer Ins in the reporting qtr.</i></b></li>
  <li>	Go to the obs datetime of the most recent return visit date, remove/eliminate obs datetime that falls in the previous reporting periods.</li>
  <li>Go to the second most recent return visit date and remove dates from 2nd or 3rd of the third month of the previous reporting qtr, to the reporting quarter and beyond. </li>
  <li><b><i style="background-color: yellow;">Go to the third most recent return visit date and remove dates from 2nd or 3rd of the third month of the previous reporting qtr, to the reporting quarter and beyond.</i></b></li>
  <li><b><span style="background-color: red;">Go to the ART days dispensed obs datetime and remove all clients that didn’t receive ART in the reporting quarter.</span>What remains is the TX-RTT.</b></li>
  </ol>
"""
st.markdown(html_table, unsafe_allow_html=True)
st.success('**PREPARED BY: Edison BN Katunguuka, Snr M&E Specialist**')
