import streamlit as st 

st.markdown('**DETAILED INSTRUCTIONS ON HOW TO USE THIS PROGRAM**')
st.write('')
st.image(r"pics/rename.png", caption="BEFORE")
st.write('')
st.write('**EMR COLUMNS BEFORE RENAMING THEM**')
st.image(r"pics/BEFORE.png", caption="BEFORE")
st.write('')
st.write('**EMR COLUMNS AFTER RENAMING THEM**')
st.image(r"pics/AFTER.png", caption="AFTER")

st.markdown('<h5><b>WHY RENAME COLUMNS?</b></h5>', unsafe_allow_html=True)
st.markdown('<p>Renaming columnsprovides one uniform name that this software can understand, other than having different names as the users may want</p>', unsafe_allow_html=True)
st.markdown('<p>This program has been instructed to understand that AS means Art start date and so forth,</p>', unsafe_allow_html=True)

st.markdown("<h5><b>WHAT IF I DON'T RENAME THE COLUMNS AS INSTRUCTED</b></h5>", unsafe_allow_html=True)
st.markdown('<p>In that case, the program will stop, and inform you of the missing or un renamed column, see image below</p>', unsafe_allow_html=True)
st.markdown('<p>It will not run untill you comply</p>', unsafe_allow_html=True)
st.image(r"pics/error1.png", caption="ERROR")

st.markdown("<h4><b>HOW TO SAVE THE EXCEL AS AN XLSX</b></h4>", unsafe_allow_html=True)
st.markdown('<p>.xlsx files, unlike other excel files like xls, offer an incorrupted file format, hence better to use</p>', unsafe_allow_html=True)
st.markdown('<p>FOLLOW THE STEPS BELOW TO SAVE THE EXTRACT AS AN XLSX</p>', unsafe_allow_html=True)
cola, colb,colc = st.columns([3,1,3])

with cola:
    st.write('**STEP 1**')
    st.write('**In the left corner of the excel, click on file**')
    st.image(r"pics/step 1.png", caption="**STEP 1**")
with colc:
    st.write('**STEP 2**')
    st.write('**Now click on Save As**')
    st.image(r"pics/step2.png", caption="**STEP 2**")

with cola:
    st.write('**STEP 3**')
    st.write('**Click on browse to choose where to save the file**')
    st.image(r"pics/step3.png", caption="**STEP 3**")
with colc:
    st.write('**STEP  4**')
    st.write('**Click on Desktop, to save the excel on your desktop**')
    st.image(r"pics/step4.png", caption="**STEP 4**")

with cola:
    st.write('**STEP  5**')
    st.write('**A list of folders on your desktop will appear, choose one (optional)**')
    st.image(r"pics/step5.png", caption="**STEP 5**")
with colc:
    st.write('**STEP  6**')
    st.write('**In the space for fie name, give the file any name, any can work**')
    st.image(r"pics/step6.png", caption="**STEP 6**")

with cola:
    st.write('**STEP  7**')
    st.write('**In the space for save as type, there must be the word Excel Workbook, if not, click on the dropdown**')
    st.image(r"pics/step7.png", caption="**STEP 7**")
with colc:
    st.write('**STEP  8**')
    st.write('**CHOOSE excel Workbook, which appears on top. This is the version for xlsx files**')
    st.image(r"pics/step8.png", caption="**STEP 8**")

with cola:
    st.write('**STEP  9**')
    st.write('**FINALLY, CLICK ON SAVE TO SAVE THE FILE**')
    st.image(r"pics/step9.png", caption="**STEP 9**")

st.markdown("<h4><b>HOW TO UPLOAD THE EXCEL INTO THE APP</b></h4>", unsafe_allow_html=True)
st.markdown('<p>If already in app, go to the section of emr reader, if not already there</p>', unsafe_allow_html=True)
st.link_button('**OR CLICK ON THIS LINK, TO LAUNCH THE APP**', url='https://program-growth.streamlit.app/')
st.markdown('<p>FOLLOW THE STEPS BELOW TO UPLOAD  THE EXTRACT FOR ANALYSIS XLSX</p>', unsafe_allow_html=True)
cola, colb,colc = st.columns([3,1,3])

with cola:
    st.write('**STEP 1**')
    st.write('**CLICK ON BROWSE FILES**')
    st.image(r"pics/upload1.png", caption="**STEP 1**")
with colc:
    st.write('**STEP 2**')
    st.write('**That will take you to your computer so that you can upload the file**')
    st.image(r"pics/upload2.png", caption="**STEP 2**")

with cola:
    st.write('**STEP 3**')
    st.write('**Go to desktop, and find a list of all folders on it**')
    st.image(r"pics/upload3.png", caption="**STEP 3**")
with colc:
    st.write('**STEP  4**')
    st.write('**Click on the folder where the emr extract you saved is**')
    st.image(r"pics/upload4.png", caption="**STEP 4**")

with cola:
    st.write('**STEP  5**')
    st.write('**Select the extract you want from among all files there**')
    st.image(r"pics/upload5.png", caption="**STEP 5**")
with colc:
    st.write('**STEP  6**')
    st.write('**Now in the right corner, click on open, and the excel will be uploded**')
    st.image(r"pics/uploa6.png", caption="**STEP 6**")

with cola:
    st.write('**STEP  7**')
    st.write('**When it is accepted, you will be prompted to choose your cluster where this facility is**')
    st.image(r"pics/upload7.png", caption="**STEP 7**")
with colc:
    st.write('**STEP  8**')
    st.write('**Then select the district, and the facility and submit**')
    st.image(r"pics/upload8.png", caption="**STEP 8**")

st.markdown("<h3><b>LINE LISTS</b></h3>", unsafe_allow_html=True)
st.markdown('<p>When you submit, linelists will popup, click on them to download any that you may be interested in</p>', unsafe_allow_html=True)
st.markdown('<p>Line lists will be named the facility name and their type eg, Lwemiyaga MISSED, for missed appointments at Lwemiyaga HC III</p>', unsafe_allow_html=True)

st.divider()
st.write('**CLICK ON ANY BUTTON TO DOWNLOAD ANY LINE-LIST**')
st.write('**IF THERE IS NO LINELIST OF INTEREST, THE APP WILL INFORM YOU**')
st.image(r"pics/lists.png", caption="**LINELISTS**")
st.divider()

st.write('**MASTERR LINELIST**')
st.write('**This one has most of the linelists combined, yo save you from downloading multiple linelists if you want**')
st.image(r"pics/master.png", caption="**MASTER**")
st.divider()

st.markdown("<h3><b>ERROR</b></h3>", unsafe_allow_html=True)
st.markdown('<p>Great emphasis has been made to ensure no errors pop, but in case of one, kindly screen shot and send to me </p>', unsafe_allow_html=True)
st.markdown('<p>When taking the screenshort, include the line where the error is made as shown below</p>', unsafe_allow_html=True)
cola, colb,colc = st.columns([3,1,3])

st.image(r"pics/error.png", caption="**ERROR**")
 
