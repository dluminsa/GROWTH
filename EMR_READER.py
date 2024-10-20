import pandas as pd 
import streamlit as st 
import os
import numpy as np
import gspread
from pathlib import Path
import traceback
import time
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
#from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# st.set_page_config(
#     page_title = 'EMR EXTRACT READER',
#     page_icon =":bar_chart"
#     )

#st.header('CODE UNDER MAINTENANCE, TRY AGAIN TOMORROW')
#st.stop()
def extract():
    cola,colb,colc = st.columns([1,3,1])
    colb.subheader('PROGRAM GROWTH')
    
    today = datetime.now()
    todayd = today.strftime("%Y-%m-%d")# %H:%M")
    wk = today.strftime("%V")
    week = int(wk)-39
    cola,colb = st.columns(2)
    cola.write(f"**DATE TODAY:    {todayd}**")
    colb.write(f"**CURRENT WEEK:    {week}**")
    st.image('rename.png', caption='instructions')
    st.image("BEFORE.png", caption="BEFORE")
    st.image("AFTER.png", caption="AFTER")
    
    # # HTML Table
    # html_table = """
    # <table style="width:100%">
    #   <tr>
    #     <th >EMR COLUMN</th>
    #     <th>RENAME TO:</th> 
    #     <th>EMR COLUMN</th>
    #     <th>RENAME TO:</th>
    #   </tr>
    # </table>
    # """
    # # Display the HTML table using markdown in Streamlit
    # st.markdown(html_table, unsafe_allow_html=True)
    # html_table = """
    # <table style="width:100%">
    #   <tr>
    #     <th>AFTER, SAVE THIS EXTRACT AS an XLSX BEFORE YOU PROCEED</th>
    #   </tr>
    # </table>
    # """
    
    # Display the HTML table using markdown in Streamlit
    #st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('**AFTER, SAVE THE EXTRACT AS an XLSX BEFORE YOU PROCEED, Check User manual for further guidance**')
    
    file = st.file_uploader("Upload your EMR extract here", type=['xlsx'])
    if 'submited' not in st.session_state:
        st.session_state.submited =False
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'reader' not in st.session_state:
        st.session_state.reader =False#
    #ext = None
    if file is not None and not st.session_state.reader:
        # Get the file name
        fileN = file.name
        ext = os.path.basename(fileN).split('.')[1]
    #df = None
    if file is not None and not st.session_state.reader:
        if ext !='xlsx':
            st.write('Unsupported file format, first save the excel as xlsx and try again')
            st.stop()
        else:
                    st.session_state.df = pd.read_excel(file)
                    df = st.session_state.df
                    st.write('Excel accepted, summaries and linelists below will be for this excel')
                    st.write('To change this excel or to upload another excel, first refresh the page')
    #if file is not None and not st.session_state.reader:
                    df = df.rename(columns= {'ART  ':'ART',  'AS  ':'AS', 'RD  ':'RD', 'RDO  ':'RDO', 'RD1  ':'RD1', 'RD2  ':'RD2', 'VD  ':'VD', 'FE  ':'FE', 'LD  ': 'LD', 'ARVD  ': 'ARVD',
       'ARVDO  ': 'ARVDO', 'TI  ': 'TI', 'TO  ':'TI', 'DD  ': 'DD', 'AG  ':'AG', 'GD  ':'GD'})
                    df = df.rename(columns= {'ART ':'ART',  'AS ':'AS', 'RD ':'RD', 'RDO ':'RDO', 'RD1 ':'RD1', 'RD2 ':'RD2', 'VD ':'VD', 'FE ':'FE', 'LD ': 'LD', 'ARVD ': 'ARVD',
                           'ARVDO ': 'ARVDO', 'TI ': 'TI', 'TO ':'TI', 'DD ': 'DD', 'AG ':'AG', 'GD ':'GD'})
                    columns = ['ART','AG', 'GD','AS', 'VD', 'RD','TO', 'TI', 'DD', 'FE','LD', 'RD1', 'RD2', 'RDO', 'ARVD', 'ARVDO']
                    #columns = ['ART','AS', 'VD', 'RD','TO', 'TI', 'DD', 'FE','LD', 'RD1', 'RD2', 'RDO', 'ARVD', 'ARVDO']
                    cols = df.columns.to_list()
                    if not all(column in cols for column in columns):
                        missing_columns = [column for column in columns if column not in cols]
                        for column in missing_columns:
                            st.markdown(f' **ERROR !!! {column} is not in the file uploaded**')
                            st.markdown('**First rename all the columns as guided above**')
                            st.stop()
                    st.session_state.reader= True
    if st.session_state.reader:
                          # Convert 'ART' column to string and create 'ART' column with numeric part to remove blanks
                        st.session_state.df = st.session_state.df.rename(columns= {'ART  ':'ART',  'AS  ':'AS', 'RD  ':'RD', 'RDO  ':'RDO', 'RD1  ':'RD1', 'RD2  ':'RD2', 'VD  ':'VD', 'FE  ':'FE', 'LD  ': 'LD', 'ARVD  ': 'ARVD',
       'ARVDO  ': 'ARVDO', 'TI  ': 'TI', 'TO  ':'TI', 'DD  ': 'DD', 'AG  ':'AG', 'GD  ':'GD'})
                        st.session_state.df = st.session_state.df.rename(columns= {'ART ':'ART',  'AS ':'AS', 'RD ':'RD', 'RDO ':'RDO', 'RD1 ':'RD1', 'RD2 ':'RD2', 'VD ':'VD', 'FE ':'FE', 'LD ': 'LD', 'ARVD ': 'ARVD',
                           'ARVDO ': 'ARVDO', 'TI ': 'TI', 'TO ':'TI', 'DD ': 'DD', 'AG ':'AG', 'GD ':'GD'})
        
                        df = st.session_state.df[['ART','AS', 'VD', 'RD','TO', 'TI', 'DD', 'FE','LD', 'RD1', 'RD2', 'RDO', 'ARVD', 'ARVDO']].copy()
                        df['ART'] = df['ART'].astype(str)
                        df['A'] = df['ART'].str.replace('[^0-9]', '', regex=True)
                        df['A'] = pd.to_numeric(df['A'], errors= 'coerce')
                        df = df[df['A']>0].copy()
                        #df.dropna(subset='ART', inplace=True)
                        
                        df[['AS', 'RD', 'VD','TO','TI']] = df[['AS', 'RD', 'VD','TO','TI']].astype(str)
                        if df['TI'].str.contains('YES').any():
                            st.write("You may be using the Transfer in column instead of the Transfer_in Obs date column")
                            st.stop()
                        
                        df['AS'] = df['AS'].astype(str)
                        df['ARVD'] = df['ARVD'].astype(str)
                        df['ARVDO'] = df['ARVDO'].astype(str)
                        df['RD'] = df['RD'].astype(str)
                        df['RD1'] = df['RD1'].astype(str)
                        df['RD2'] = df['RD2'].astype(str)
                        df['RDO'] = df['RDO'].astype(str)
                        df['TI'] = df['TI'].astype(str)
                        df['TO'] = df['TO'].astype(str)
                        df['VD'] = df['VD'].astype(str)
                        df['DD'] = df['DD'].astype(str)
                        df['LD'] = df['LD'].astype(str)
                        df['FE'] = df['FE'].astype(str)
                        
                        y = pd.DataFrame({'ART' :['2','3','4'], 'TI':['1-1-1',1,'1/1/1'], 'RD':['1-1-1',1,'1/1/1'],'DD':['1-1-1',1,'1/1/1'], 
                                        'TO':['1-1-1',1,'1/1/1'], 'AS':['1-1-1',1,'1/1/1'], 'VD':['1-1-1',1,'1/1/1'],'RD1':['1-1-1',1,'1/1/1'],
                                        'RD2':['1-1-1',1,'1/1/1'],'RDO':['1-1-1',1,'1/1/1'], 'ARVD':['1-1-1',1,'1/1/1'], 'ARVDO':['1-1-1',1,'1/1/1'],
                                        'LD':['1-1-1',1,'1/1/1'],'FE':['1-1-1',1,'1/1/1']})  
                        
                        
                        df['AS'] = df['AS'].astype(str)
                        df['ARVDO'] = df['ARVDO'].astype(str)
                        df['RD'] = df['RD'].astype(str)
                        df['RD1'] = df['RD1'].astype(str)
                        df['RD2'] = df['RD2'].astype(str)
                        df['RDO'] = df['RDO'].astype(str)
                        df['TI'] = df['TI'].astype(str)
                        df['TO'] = df['TO'].astype(str)
                        df['VD'] = df['VD'].astype(str)
                        df['DD'] = df['DD'].astype(str)
                        df['LD'] = df['LD'].astype(str)
                        df['FE'] = df['FE'].astype(str)
            
                        df['AS'] = df['AS'].str.replace('00:00:00', '', regex=True)
                        df['ARVDO'] = df['ARVDO'].str.replace('00:00:00', '', regex=True)
                        df['RD'] = df['RD'].str.replace('00:00:00', '', regex=True)
                        df['RD1'] = df['RD1'].str.replace('00:00:00', '', regex=True)
                        df['RD2'] = df['RD2'].str.replace('00:00:00', '', regex=True)
                        df['RDO'] = df['RDO'].str.replace('00:00:00', '', regex=True)
                        df['TI'] = df['TI'].str.replace('00:00:00', '', regex=True)
                        df['TO'] = df['TO'].str.replace('00:00:00', '', regex=True)
                        df['VD'] = df['VD'].str.replace('00:00:00', '', regex=True)
                        df['DD'] = df['DD'].str.replace('00:00:00', '', regex=True)
                        df['LD'] = df['LD'].str.replace('00:00:00', '', regex=True)
                        df['FE'] = df['FE'].str.replace('00:00:00', '', regex=True)
            
            
                        df = pd.concat([df,y])
            
            
                        df['AS'] = df['AS'].astype(str) ###
                        df['ARVDO'] = df['ARVDO'].astype(str)
                        df['RD'] = df['RD'].astype(str) ###
                        df['RD1'] = df['RD1'].astype(str)##
                        df['RD2'] = df['RD2'].astype(str)##
                        df['RDO'] = df['RDO'].astype(str)
                        df['TI'] = df['TI'].astype(str) ##
                        df['TO'] = df['TO'].astype(str) ##
                        df['VD'] = df['VD'].astype(str) ###
                        df['DD'] = df['DD'].astype(str) ####
                        df['LD'] = df['LD'].astype(str)
                        df['FE'] = df['FE'].astype(str)
            
            
                        # SPLITTING ART START DATE
                        A = df[df['AS'].str.contains('-')].copy()
                        a = df[~df['AS'].str.contains('-')].copy()
                        B = a[a['AS'].str.contains('/')].copy()
                        C = a[~a['AS'].str.contains('/')].copy()
            
                        A[['Ayear', 'Amonth', 'Aday']] = A['AS'].str.split('-', expand = True)
                        B[['Ayear', 'Amonth', 'Aday']] = B['AS'].str.split('/', expand = True)
                        try:            
                            C['AS'] = pd.to_numeric(C['AS'], errors='coerce')
                            C['AS'] = pd.to_datetime(C['AS'], origin='1899-12-30', unit='D', errors='coercee')
                            C['AS'] =  C['AS'].astype(str)
                            C[['Ayear', 'Amonth', 'Aday']] = C['AS'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
            
                        # SPLITTING DEATH DATE
                        A = df[df['DD'].str.contains('-')].copy()
                        a = df[~df['DD'].str.contains('-')].copy()
                        B = a[a['DD'].str.contains('/')].copy()
                        C = a[~a['DD'].str.contains('/')].copy()
            
                        A[['Dyear', 'Dmonth', 'Dday']] = A['DD'].str.split('-', expand = True)
                        B[['Dyear', 'Dmonth', 'Dday']] = B['DD'].str.split('/', expand = True)
                        try:            
                            C['DD'] = pd.to_numeric(C['DD'], errors='coerce')
                            C['DD'] = pd.to_datetime(C['DD'], origin='1899-12-30', unit='D', errors='coerce')
                            C['DD'] =  C['DD'].astype(str)
                            C[['Dyear', 'Dmonth', 'Dday']] = C['DD'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
                    
                        # SORTING THE RETURN VISIT DATE
                        A = df[df['RD'].str.contains('-')].copy()
                        a = df[~df['RD'].str.contains('-')].copy()
                        B = a[a['RD'].str.contains('/')].copy()
                        C = a[~a['RD'].str.contains('/')].copy()
                        numeric_entries = df[df['RD'].apply(lambda x: isinstance(x, (int, float)) or x.isdigit())]
                        #FYB = numeric_entries.copy()
                        numeric_entrie = df[~df['RD'].apply(lambda x: isinstance(x, (int, float)) or x.isdigit())]
                        FYB = numeric_entrie.copy()
                
                        A[['Ryear', 'Rmonth', 'Rday']] = A['RD'].str.split('-', expand = True)
                        B[['Ryear', 'Rmonth', 'Rday']] = B['RD'].str.split('/', expand = True)
                        try:
                            C['RD'] = pd.to_numeric(C['RD'], errors='coerce')
                            C['RD'] = pd.to_datetime(C['RD'], origin='1899-12-30', unit='D', errors='coerce')
                            C['RD'] =  C['RD'].astype(str)
                            C[['Ryear', 'Rmonth', 'Rday']] = C['RD'].str.split('-', expand = True)
                        except:
                            C['RD'] = pd.to_datetime(C['RD'], format='%d %m %Y', errors='coerce')
                            C[['Ryear', 'Rmonth', 'Rday']] = C['RD'].str.split('-', expand = True)
                            
                            #pass
                        df = pd.concat([A,B,C]) 
                    
                        #SORTING THE VD DATE
                        A = df[df['VD'].str.contains('-')].copy()
                        a = df[~df['VD'].str.contains('-')].copy()
                        B = a[a['VD'].str.contains('/')].copy()
                        C = a[~a['VD'].str.contains('/')].copy()
            
                        A[['Vyear', 'Vmonth', 'Vday']] = A['VD'].str.split('-', expand = True)
                        B[['Vyear', 'Vmonth', 'Vday']] = B['VD'].str.split('/', expand = True)
                        try:
                            C['VD'] = pd.to_numeric(C['VD'], errors='coerce')
                            C['VD'] = pd.to_datetime(C['VD'], origin='1899-12-30', unit='D', errors='coerce')
                            C['VD'] =  C['VD'].astype(str)
                            C[['Vyear', 'Vmonth', 'Vday']] = C['VD'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
            
                        #SORTING THE TO DATE
                        A = df[df['TO'].str.contains('-')].copy()
                        a = df[~df['TO'].str.contains('-')].copy()
                        B = a[a['TO'].str.contains('/')].copy()
                        C = a[~a['TO'].str.contains('/')].copy()
            
                        A[['Tyear', 'Tmonth', 'Tday']] = A['TO'].str.split('-', expand = True)
                        B[['Tyear', 'Tmonth', 'Tday']] = B['TO'].str.split('/', expand = True)
                        try:            
                            C['TO'] = pd.to_numeric(C['TO'], errors='coerce')
                            C['TO'] = pd.to_datetime(C['TO'], origin='1899-12-30', unit='D', errors='coerce')
                            C['TO'] =  C['TO'].astype(str)
                            C[['Tyear', 'Tmonth', 'Tday']] = C['TO'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
                    
            
                    #SORTING THE TI DATE
                        A = df[df['TI'].str.contains('-')].copy()
                        a = df[~df['TI'].str.contains('-')].copy()
                        B = a[a['TI'].str.contains('/')].copy()
                        C = a[~a['TI'].str.contains('/')].copy()
            
                        A[['Tiyear', 'Timonth', 'Tiday']] = A['TI'].str.split('-', expand = True)
                        B[['Tiyear', 'Timonth', 'Tiday']] = B['TI'].str.split('/', expand = True)
                        try:            
                            C['TI'] = pd.to_numeric(C['TI'], errors='coerce')
                            C['TI'] = pd.to_datetime(C['TI'], origin='1899-12-30', unit='D', errors='coerce')
                            C['TI'] =  C['TI'].astype(str)
                            C[['Tiyear', 'Timonth', 'Tiday']] = C['TI'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
            
                        # SORTING THE RETURN VISIT DATE1
                        A = df[df['RD1'].str.contains('-')].copy()
                        a = df[~df['RD1'].str.contains('-')].copy()
                        B = a[a['RD1'].str.contains('/')].copy()
                        C = a[~a['RD1'].str.contains('/')].copy()
                
                        A[['R1year', 'R1month', 'R1day']] = A['RD1'].str.split('-', expand = True)
                        B[['R1year', 'R1month', 'R1day']] = B['RD1'].str.split('/', expand = True)
                        try:
                            C['RD1'] = pd.to_numeric(C['RD1'], errors='coerce')
                            C['RD1'] = pd.to_datetime(C['RD1'], origin='1899-12-30', unit='D', errors='coerce')
                            C['RD1'] =  C['RD1'].astype(str)
                            C[['R1year', 'R1month', 'R1day']] = C['RD1'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C]) 
                    
                        # SORTING THE RETURN VISIT DATE2
                        A = df[df['RD2'].str.contains('-')].copy()
                        a = df[~df['RD2'].str.contains('-')].copy()
                        B = a[a['RD2'].str.contains('/')].copy()
                        C = a[~a['RD2'].str.contains('/')].copy()
                
                        A[['R2year', 'R2month', 'R2day']] = A['RD2'].str.split('-', expand = True)
                        B[['R2year', 'R2month', 'R2day']] = B['RD2'].str.split('/', expand = True)
                        try:
                            C['RD2'] = pd.to_numeric(C['RD2'], errors='coerce')
                            C['RD2'] = pd.to_datetime(C['RD2'], origin='1899-12-30', unit='D', errors='coerce')
                            C['RD2'] =  C['RD2'].astype(str)
                            C[['R2year', 'R2month', 'R2day']] = C['RD2'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
                    
                        # SORTING THE RETURN VISIT OBS DATE
                        A = df[df['RDO'].str.contains('-')].copy()
                        a = df[~df['RDO'].str.contains('-')].copy()
                        B = a[a['RDO'].str.contains('/')].copy()
                        C = a[~a['RDO'].str.contains('/')].copy()
                
                        A[['ROyear', 'ROmonth', 'ROday']] = A['RDO'].str.split('-', expand = True)
                        B[['ROyear', 'ROmonth', 'ROday']] = B['RDO'].str.split('/', expand = True)
                        try:
                            C['RDO'] = pd.to_numeric(C['RDO'], errors='coerce')
                            C['RDO'] = pd.to_datetime(C['RDO'], origin='1899-12-30', unit='D', errors='coerce')
                            C['RDO'] =  C['RDO'].astype(str)
                            C[['ROyear', 'ROmonth', 'ROday']] = C['RDO'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
            
                        # SORTING THE LAST ENCOUNTER DATES
                        A = df[df['LD'].str.contains('-')].copy()
                        a = df[~df['LD'].str.contains('-')].copy()
                        B = a[a['LD'].str.contains('/')].copy()
                        C = a[~a['LD'].str.contains('/')].copy()
                
                        A[['Lyear', 'Lmonth', 'Lday']] = A['LD'].str.split('-', expand = True)
                        B[['Lyear', 'Lmonth', 'Lday']] = B['LD'].str.split('/', expand = True)
                        try:
                            C['LD'] = pd.to_numeric(C['LD'], errors='coerce')
                            C['LD'] = pd.to_datetime(C['LD'], origin='1899-12-30', unit='D', errors='coerce')
                            C['LD'] =  C['LD'].astype(str)
                            C[['Lyear', 'Lmonth', 'Lday']] = C['LD'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
                    
                        # SORTING THE ARV DISPENSED DATES
                        A = df[df['ARVDO'].str.contains('-')].copy()
                        a = df[~df['ARVDO'].str.contains('-')].copy()
                        B = a[a['ARVDO'].str.contains('/')].copy()
                        C = a[~a['ARVDO'].str.contains('/')].copy()
                
                        A[['Aryear', 'Armonth', 'Arday']] = A['ARVDO'].str.split('-', expand = True)
                        B[['Aryear', 'Armonth', 'Arday']] = B['ARVDO'].str.split('/', expand = True)
                        try:
                            C['ARVDO'] = pd.to_numeric(C['ARVDO'], errors='coerce')
                            C['ARVDO'] = pd.to_datetime(C['ARVDO'], origin='1899-12-30', unit='D', errors='coerce')
                            C['ARVDO'] =  C['ARVDO'].astype(str)
                            C[['Aryear', 'Armonth', 'Arday']] = C['ARVDO'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
            
                        # SORTING THE FIRST ENCOUNTER
                        A = df[df['FE'].str.contains('-')].copy()
                        a = df[~df['FE'].str.contains('-')].copy()
                        B = a[a['FE'].str.contains('/')].copy()
                        C = a[~a['FE'].str.contains('/')].copy()
                
                        A[['Fyear', 'Fmonth', 'Fday']] = A['FE'].str.split('-', expand = True)
                        B[['Fyear', 'Fmonth', 'Fday']] = B['FE'].str.split('/', expand = True)
                        try:
                            C['FE'] = pd.to_numeric(C['FE'], errors='coerce')
                            C['FE'] = pd.to_datetime(C['FE'], origin='1899-12-30', unit='D', errors='coerce')
                            C['FE'] =  C['FE'].astype(str)
                            C[['Fyear', 'Fmonth', 'Fday']] = C['FE'].str.split('-', expand = True)
                        except:
                            pass
                        df = pd.concat([A,B,C])
            
                        #BRINGING BACK THE / IN DATES
                        df['AS'] = df['AS'].astype(str)
                        df['ARVDO'] = df['ARVDO'].astype(str)
                        df['RD'] = df['RD'].astype(str)
                        df['RD1'] = df['RD1'].astype(str)
                        df['RD2'] = df['RD2'].astype(str)
                        df['RDO'] = df['RDO'].astype(str)
                        df['TI'] = df['TI'].astype(str)
                        df['TO'] = df['TO'].astype(str)
                        df['VD'] = df['VD'].astype(str)
                        df['DD'] = df['DD'].astype(str)
                        df['LD'] = df['LD'].astype(str)
                        df['FE'] = df['FE'].astype(str)
            
            #             #Clearing NaT from te dates
                        df['AS'] = df['AS'].str.replace('NaT', '',regex=True)
                        df['ARVDO'] = df['ARVDO'].str.replace('NaT', '',regex=True)
                        df['RD'] = df['RD'].str.replace('NaT', '',regex=True)
                        df['RD1'] = df['RD1'].str.replace('NaT', '',regex=True)
                        df['RD2'] = df['RD2'].str.replace('NaT', '',regex=True)
                        df['RDO'] = df['RDO'].str.replace('NaT', '',regex=True)
                        df['TI'] = df['TI'].str.replace('NaT', '',regex=True)
                        df['TO'] = df['TO'].str.replace('NaT', '',regex=True)
                        df['VD'] = df['VD'].str.replace('NaT', '',regex=True)
                        df['DD'] = df['DD'].str.replace('NaT', '',regex=True)
                        df['LD'] = df['LD'].str.replace('NaT', '',regex=True)
                        df['FE'] = df['FE'].str.replace('NaT', '',regex=True)
            
                                    #SORTING THE VIRAL LOAD YEARS
                    
                        df[['Vyear', 'Vmonth', 'Vday']] =df[['Vyear', 'Vmonth', 'Vday']].apply(pd.to_numeric, errors = 'coerce') 
                        df['Vyear'] = df['Vyear'].fillna(994)
                        a = df[df['Vyear']>31].copy()
                        b = df[df['Vyear']<32].copy()
                        b = b.rename(columns={'Vyear': 'Vday2', 'Vday': 'Vyear'})
                        b = b.rename(columns={'Vday2': 'Vday'})
                        df = pd.concat([a,b])
                        dfa = df.shape[0]
            
            
                        #SORTING THE TI YEARS
                        df[['Tiyear', 'Tiday']] =df[['Tiyear','Tiday']].apply(pd.to_numeric, errors = 'coerce')
                        df['Tiyear'] = df['Tiyear'].fillna(994)
                        a = df[df['Tiyear']>31].copy()
                        b = df[df['Tiyear']<32].copy()
                        b = b.rename(columns={'Tiyear': 'Tiday2', 'Tiday': 'Tiyear'})
                        b = b.rename(columns={'Tiday2': 'Tiday'})
                        df = pd.concat([a,b])
                        dfb = df.shape[0]
            
                        # #SORTING THE RETURN VISIT DATE YEARS
                        df[['Rday', 'Ryear']] = df[['Rday', 'Ryear']].apply(pd.to_numeric, errors='coerce')
                        
                        df['Ryear'] = df['Ryear'].fillna(994)
                        a = df[df['Ryear']>31].copy()
                        b = df[df['Ryear']<32].copy()
                        b = b.rename(columns={'Ryear': 'Rday2', 'Rday': 'Ryear'})
                        b = b.rename(columns={'Rday2': 'Rday'})
            
                        df = pd.concat([a,b])
                        dfc = df.shape[0]
                        
                            #SORTING THE TRANSFER OUT DATE YEAR
                        df[['Tday', 'Tyear']] = df[['Tday', 'Tyear']].apply(pd.to_numeric, errors='coerce')
                        df['Tyear'] = df['Tyear'].fillna(994)
                        a = df[df['Tyear']>31].copy()
                        b = df[df['Tyear']<32].copy()
                        b = b.rename(columns={'Tyear': 'Tday2', 'Tday': 'Tyear'})
                        b = b.rename(columns={'Tday2': 'Tday'})
                        df = pd.concat([a,b])
            
                        
                        #SORTING THE ART START YEARS
                        df[['Ayear', 'Amonth', 'Aday']] =df[['Ayear', 'Amonth', 'Aday']].apply(pd.to_numeric, errors = 'coerce')
                        df['Ayear'] = df['Ayear'].fillna(994)
                        a = df[df['Ayear']>31].copy()
                        b = df[df['Ayear']<32].copy()
                        b = b.rename(columns={'Ayear': 'Aday2', 'Aday': 'Ayear'})
                        b = b.rename(columns={'Aday2': 'Aday'})
                        df = pd.concat([a,b])
                        dfe = df.shape[0]
            
                        #SORTING THE ART START YEARS
                        df[['Dyear', 'Dmonth', 'Dday']] =df[['Dyear', 'Dmonth', 'Dday']].apply(pd.to_numeric, errors = 'coerce')
                        df['Dyear'] = df['Dyear'].fillna(994)
                        a = df[df['Dyear']>31].copy()
                        b = df[df['Dyear']<32].copy()
                        b = b.rename(columns={'Dyear': 'Dday2', 'Dday': 'Dyear'})
                        b = b.rename(columns={'Dday2': 'Dday'})
                        df = pd.concat([a,b])
                        dfe = df.shape[0]
            
                        # #SORTING THE RETURN VISIT DATE1
                        df[['R1day', 'R1year']] = df[['R1day', 'R1year']].apply(pd.to_numeric, errors='coerce')
                        
                        df['R1year'] = df['R1year'].fillna(994)
                        a = df[df['R1year']>31].copy()
                        b = df[df['R1year']<32].copy()
                        b = b.rename(columns={'R1year': 'R1day2', 'R1day': 'R1year'})
                        b = b.rename(columns={'R1day2': 'R1day'})
            
                        df = pd.concat([a,b])
                        dfc = df.shape[0]
            
                        # #SORTING THE RETURN VISIT DATE2
                        df[['R2day', 'R2year']] = df[['R2day', 'R2year']].apply(pd.to_numeric, errors='coerce')
                        
                        df['R2year'] = df['R2year'].fillna(994)
                        a = df[df['R2year']>31].copy()
                        b = df[df['R2year']<32].copy()
                        b = b.rename(columns={'R2year': 'R2day2', 'R2day': 'R2year'})
                        b = b.rename(columns={'R2day2': 'R2day'})
            
                        df = pd.concat([a,b])
                        dfc = df.shape[0]
            
                        # #SORTING THE RETURN VISIT OBS DATE
                        df[['ROday', 'ROyear']] = df[['ROday', 'ROyear']].apply(pd.to_numeric, errors='coerce')
                        
                        df['ROyear'] = df['ROyear'].fillna(994)
                        a = df[df['ROyear']>31].copy()
                        b = df[df['ROyear']<32].copy()
                        b = b.rename(columns={'ROyear': 'ROday2', 'ROday': 'ROyear'})
                        b = b.rename(columns={'ROday2': 'ROday'})
            
                        df = pd.concat([a,b])
                        dfc = df.shape[0]
            
                        # #SORTING THE LAST ENCOUNTER
                        df[['Lday', 'Lyear']] = df[['Lday', 'Lyear']].apply(pd.to_numeric, errors='coerce')
                        
                        df['Lyear'] = df['Lyear'].fillna(994)
                        a = df[df['Lyear']>31].copy()
                        b = df[df['Lyear']<32].copy()
                        b = b.rename(columns={'Lyear': 'Lday2', 'Lday': 'Lyear'})
                        b = b.rename(columns={'Lday2': 'Lday'})
            
                        df = pd.concat([a,b])
                        dfc = df.shape[0]
            
                        # #SORTING THE FIRST ENCOUNTER
                        df[['Fday', 'Fyear']] = df[['Fday', 'Fyear']].apply(pd.to_numeric, errors='coerce')
                        
                        df['Fyear'] = df['Fyear'].fillna(994)
                        a = df[df['Fyear']>31].copy()
                        b = df[df['Fyear']<32].copy()
                        b = b.rename(columns={'Fyear': 'Fday2', 'Fday': 'Fyear'})
                        b = b.rename(columns={'Fday2': 'Fday'})
            
                        df = pd.concat([a,b])
                        dfc = df.shape[0]
            
                        # #SORTING THE FIRST ENCOUNTER
                        df[['Arday', 'Aryear']] = df[['Arday', 'Aryear']].apply(pd.to_numeric, errors='coerce')
                        
                        df['Aryear'] = df['Aryear'].fillna(994)
                        a = df[df['Aryear']>31].copy()
                        b = df[df['Aryear']<32].copy()
                        b = b.rename(columns={'Aryear': 'Arday2', 'Arday': 'Aryear'})
                        b = b.rename(columns={'Arday2': 'Arday'})
                        df = pd.concat([a,b])
                        dfc = df.shape [0]
            
                        #CREATE WEEKS 
                        df['Rdaya'] = df['Rday'].astype(str).str.split('.').str[0]
                        df['Rmontha'] = df['Rmonth'].astype(str).str.split('.').str[0]
                        df['Ryeara'] = df['Ryear'].astype(str).str.split('.').str[0]
            
                        df['RETURN DATE'] = df['Rdaya'] + '/' + df['Rmontha'] + '/' + df['Ryeara']
                        df['RETURN DATE'] = pd.to_datetime(df['RETURN DATE'], format='%d/%m/%Y', errors='coerce')
                        #CREATING WEEEK FOR RETURN VISIT DATE
                        df['RWEEK'] = df['RETURN DATE'].dt.strftime('%V')
                        df['RWEEK'] = pd.to_numeric(df['RWEEK'], errors='coerce')
                        #SURGE WEEK
                        df['RWEEK'] = pd.to_numeric(df['RWEEK'], errors='coerce')
                        df['RWEEK1'] = df['RWEEK']-39
                        #       #PARAMETERS FOR CIRA
                           
                        df['R1aya'] = df['R1day'].astype(str).str.split('.').str[0]
                        df['R1montha'] = df['R1month'].astype(str).str.split('.').str[0]
                        df['R1yeara'] = df['R1year'].astype(str).str.split('.').str[0]
                        df['RETURN DATE1'] = df['R1aya'] + '/' + df['R1montha'] + '/' + df['R1yeara']
                        df['RETURN DATE1'] = pd.to_datetime(df['RETURN DATE1'], format='%d/%m/%Y', errors='coerce')
                        df['RWEEKR'] = df['RETURN DATE1'].dt.strftime('%V') #Use R since 1 was already used
                        df['RWEEKR'] = pd.to_numeric(df['RWEEKR'], errors='coerce')
                        #df['RWEEKR1'] = df['RWEEKR']-39 NOT NEEDED THIS Q SINCE WE ARE USING 
                        # df['DUR'] = round((df['RETURN DATE'] - df['RETURN DATE2']).dt.days / 30)
                        # def cira(a):
                        #     if a<1:
                        #         return 'UK'
                        #     elif a< 3:
                        #         return '<3 MTHS'
                        #     elif a <6:
                        #         return '3-5 MTHS'
                        #     elif a >5:
                        #         return '6 MTHS+'
                        #     else:
                        #         return 'UK'
                        # df['CIRA'] = df['DUR'].apply(cira)
                        # def ager(a):
                        #     if a< 1:
                        #         return '<01'
                        #     elif a < 10:
                        #         return '01-09'
                        #     elif a < 20:
                        #         return '10-19'
                        #     elif a < 30:
                        #         return '20-29'
                        #     elif a < 40:
                        #         return '30-39'
                        #     elif a < 50:
                        #         return '40-49'
                        #     elif a >49:
                        #         return '50+'
                        # df['AG'] = pd.to_numeric(df['AG'], errors = 'coerce')
        
                        #COPY FOR ONE YEAR BEFORE GETTING POT CURR
                        oneyear = df.copy()
                        #df['GROUP'] = df['AG'].apply(ager)
                        #LAST Q'S TXML ALTER
                        df['Tyear'] = pd.to_numeric(df['Tyear'],errors='coerce')
                        last = df[df['Tyear']==994].copy()
                        last['Dyear'] = pd.to_numeric(last['Dyear'],errors='coerce')
                        last = last[last['Dyear']==994].copy()
                        last[['Ryear', 'Rmonth']] = last[['Ryear', 'Rmonth']].apply(pd.to_numeric, errors='coerce')
                        last = last[((last['Ryear']==2024) & (last['Rmonth'].isin([6,7,8])))].copy()
                        last[['Rmonth', 'Rday']] = last[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
                        last = last[((last['Rmonth']>6) | ((last['Rmonth']==6) & (last['Rday']>2)))].copy()
                        lastq = last.shape[0]
                    
                        #POTENTIAL TXCUR ALTER... 
                        df[['Rmonth', 'Rday', 'Ryear']] = df[['Rmonth', 'Rday', 'Ryear']].apply(pd.to_numeric, errors='coerce')
                        df25 = df[df['Ryear']>2024].copy()
                        df24 = df[df['Ryear'] == 2024].copy()
                        df24[['Rmonth', 'Rday']] = df24[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
                        df24 = df24[((df24['Rmonth']>9) | ((df24['Rmonth']==9) & (df24['Rday']>2)))].copy()
                        df = pd.concat([df25, df24]).copy()
            
                        #REMOVE TO of the last reporting month
                        df[ 'Tyear'] = pd.to_numeric(df['Tyear'], errors='coerce')
                        dfto = df[df['Tyear']!=994].copy()
                        dfnot = df[df['Tyear'] == 994].copy()
                        dfto[['Ryear', 'Rmonth']] = dfto[['Ryear', 'Rmonth']].apply(pd.to_numeric, errors='coerce')
                        dfto = dfto[((dfto['Ryear']!=2024) |((dfto['Ryear']==2024) & (dfto['Rmonth']!=9)))].copy()
                        df = pd.concat([dfto,dfnot])
            
                        #REMOVE TO of the dead reporting month
                        df[ 'Dyear'] = pd.to_numeric(df['Dyear'], errors='coerce')
                        dfdd = df[df['Dyear']!=994].copy()
                        dfnot = df[df['Dyear'] == 994].copy()
                        #THOSE WHO DIED BEFORE FIRST MONTH OF THE Q
                        dfdd[['Dyear', 'Dmonth']] = dfdd[['Dyear', 'Dmonth']].apply(pd.to_numeric, errors='coerce')
                        dfdd = dfdd[((dfdd['Dyear']>2024) |((dfdd['Dyear']==2024) & (dfdd['Dmonth']>9)))].copy()
                        df = pd.concat([dfdd,dfnot])
                        pot = df.shape[0]
            
                        #TRANSFER OUTS
                        
                        #TRANSFER INS
                        df[['Tiyear', 'Timonth']] = df[['Tiyear', 'Timonth']].apply(pd.to_numeric, errors='coerce')
                        dfti = df[((df['Tiyear']==2024) & (df['Timonth']>9))].copy() #TI
                        ti = dfti.shape[0]
            
                        dfnot = df[((df['Tiyear']!=2024) | ((df['Tiyear']==2024) & (df['Timonth']<10)))].copy() #NO TI
                        noti = dfnot.shape[0]
            
                        #TX NEW THIS Q
                        dfnot[['Ayear', 'Amonth']] = dfnot[['Ayear', 'Amonth']].apply(pd.to_numeric, errors='coerce')
                        dfnew = dfnot[((dfnot['Ayear']==2024) & (dfnot['Amonth']>9))].copy() #TI
                        txnew = dfnew.shape[0]
            
                        dfold = dfnot[((dfnot['Ayear']!=2024) | ((dfnot['Ayear']==2024) & (dfnot['Amonth']<10)))].copy() #NO TI
                        dfcheck = dfold.copy() #use this to determine unknown gain
                        old = dfold.shape[0]
                        ##RTT
                        #RTT BY LAST ENCOUNTER to include only months in the reporting Q
                        dfold['Lyear'] = pd.to_numeric(dfold['Lyear'], errors='coerce') 
                        dfRTT = dfold[dfold['Lyear']==2024].copy() #ALTER
                        dfRTT['Lmonth'] = pd.to_numeric(dfRTT['Lmonth'], errors='coerce') 
                        dfRTT = dfRTT[dfRTT['Lmonth'].isin([10,11,12])].copy() #ALTER
            
                        #BY FIRST ENCOUNTER, To remove those first encountered in the Q
                        dfRTT['Fyear'] = pd.to_numeric(dfRTT['Fyear'], errors='coerce') 
                        dfRTTa = dfRTT[dfRTT['Fyear']==2024].copy() #ALTER
                        dfRTTb = dfRTT[dfRTT['Fyear']!=2024].copy() #ALTER
                        #BY FIRST ENCOUNTER
                        dfRTTa['Fmonth'] = pd.to_numeric(dfRTTa['Fmonth'], errors='coerce') 
                        dfRTTa = dfRTTa[~dfRTTa['Fmonth'].isin([10,11,12])].copy() # ALTER
                        dfRTT = pd.concat([dfRTTa, dfRTTb])
            
                        # #BY ART START, To remove those that started ART in the Q
                        # dfRTT['Ayear'] = pd.to_numeric(dfRTT['Ayear'], errors='coerce')
                        # dfRTTa = dfRTT[dfRTT['Ayear']==2024].copy() #ALTER
                        # dfRTTb = dfRTT[dfRTT['Ayear']!=2024].copy() #ALTER ##ALREADY REMOVED ABOVE
                        # #BY ART START
                        # dfRTTa['Amonth'] = pd.to_numeric(dfRTTa['Amonth'], errors='coerce') 
                        # dfRTTa = dfRTTa[~dfRTTa['Amonth'].isin([10,11,12])].copy() # ALTER use <
                        # dfRTT = pd.concat([dfRTTa, dfRTTb])
                        # #BY TI DATE, To remove those that TI in the Q
                        # dfRTT['Tiyear'] = pd.to_numeric(dfRTT['Tiyear'], errors='coerce')
                        # dfRTTa = dfRTT[dfRTT['Tiyear']==2024].copy() #ALTER
                        # dfRTTb = dfRTT[dfRTT['Tiyear']!=2024].copy() #ALTER
                        # #BY TI  
                        # dfRTTa['Timonth'] = pd.to_numeric(dfRTTa['Timonth'], errors='coerce') 
                        # dfRTTa = dfRTTa[~dfRTTa['Timonth'].isin([7,8,9])].copy() # ALTER use <
                        # dfRTT = pd.concat([dfRTTa, dfRTTb])
            
                        #BY RD OBS DATE,  remove those that fall in the previous reporting Quarter
                        dfRTT['ROyear'] = pd.to_numeric(dfRTT['ROyear'], errors='coerce')
                        dfRTTa = dfRTT[dfRTT['ROyear']>2024].copy()
                        dfRTTb = dfRTT[dfRTT['ROyear']==2024].copy() 
                        dfRTTb[['ROmonth', 'ROday']] = dfRTTb[['ROmonth', 'ROday']].apply(pd.to_numeric, errors='coerce')
                        dfRTTb = dfRTTb[((dfRTTb['ROmonth']>9) | ((dfRTTb['ROmonth']==9) & (dfRTTb['ROday']>2)))].copy()
                        dfRTT = pd.concat([dfRTTa, dfRTTb])
            
                        #BY RDDATE1,  take those that fall in the previous reporting Quarter
                        dfRTT['R1year'] = pd.to_numeric(dfRTT['R1year'], errors='coerce') 
                        dfRTTa = dfRTT[dfRTT['R1year']<2024].copy()
                        dfRTTb = dfRTT[dfRTT['R1year']==2024].copy()
                        dfRTTb[['R1month', 'R1day']] = dfRTTb[['R1month', 'R1day']].apply(pd.to_numeric, errors='coerce')
                        dfRTTb = dfRTTb[((dfRTTb['R1month']<9) | ((dfRTTb['R1month']==9) & (dfRTTb['R1day']<3)))].copy()
                        dfRTT = pd.concat([dfRTTa, dfRTTb])
            
                        #BY RD DATE2,  take those that fall in the previous reporting Quarter
                        dfRTT['R2year'] = pd.to_numeric(dfRTT['R2year'], errors='coerce')
                        dfRTTa = dfRTT[dfRTT['R2year']<2024].copy()
                        dfRTTb = dfRTT[dfRTT['R2year']==2024].copy()
                        dfRTTb[['R2month', 'R2day']] = dfRTTb[['R2month', 'R2day']].apply(pd.to_numeric, errors='coerce')
                        dfRTTb = dfRTTb[((dfRTTb['R2month']<9) | ((dfRTTb['R2month']==9) & (dfRTTb['R2day']<3)))].copy()
                        dfRTT = pd.concat([dfRTTa, dfRTTb])
            
                        #BY ARV DISPENSED, to take those that got ART in the Q
                        dfRTT['Aryear'] = pd.to_numeric(dfRTT['Aryear'], errors='coerce') 
                        dfRTT = dfRTT[dfRTT['Aryear']==2024].copy() 
                        dfRTT['Armonth'] = pd.to_numeric(dfRTT['Armonth'], errors='coerce') 
                        dfRTT = dfRTT[dfRTT['Armonth'].isin([10,11,12])].copy()
                        rtt = dfRTT.shape[0]
                        #check
                        #rt = dfRTT.copy()
            
            #######LOSSES. START FROM POTENTIAL CURR
                    #TRANSFER OUTS
                        df['Tyear'] = pd.to_numeric(df['Tyear'], errors='coerce')
                        dfto = df[df['Ryear']==994].copy()
                        dfnot = df[df['Ryear']!=994].copy()
                        wk = int(wk)
            
                        #FALSE TO OUTS BASED ON CURRENT WEEK
                        dfto[['Ryear', 'RWEEK']] =  dfto[['Ryear', 'RWEEK']].apply(pd.to_numeric, errors='coerce')
                        dfw = dfto[((dfto['Ryear']>2024) | ((dfto['Ryear']==2024) & (dfto['RWEEK']>=wk)))].copy() #FALSE
                        false = dfw.shape[0]
                        dft = dfto[((dfto['Ryear']<2024) | ((dfto['Ryear']==2024) & (dfto['RWEEK']<wk)))].copy()  ##TRUE
                        true = dft.shape[0]
                        #add the false back to txcur
                        df = pd.concat([dfnot,dfw]) #WILL USE THIS FOR ACTIVE LATER
            
                        #THOSE THAT HAVE DIED SO FAR
                        df[ 'Dyear'] = pd.to_numeric(df['Dyear'], errors='coerce')
                        died = df[df['Dyear']!=994].copy() #DIED
                        dead = died.shape[0]
            
                        #THIS CURR WILL HAVE NO DEAD AND TRUE TO
                        df = df[df['Dyear'] == 994].copy() #LIVING, NO DEATH DATE
            
                        #REMOVNG CURRENT LOST
                        #USE CALENDAR WEEK FOR THIS Q, SWITCH TO SURGE WEEK NEXT Q
                        #lost 2 weeks
                        wk = int(wk)
                        wk2 = wk-1
                        wk3 = wk-2
                        wk4 = wk-3
                        df['Ryear'] = pd.to_numeric(df['Ryear'], errors='coerce')
                        df24 = df[df['Ryear'] ==2024].copy()
                        df25 = df[df['Ryear']>2024].copy()
                        
                        df24['RWEEK'] = pd.to_numeric(df24['RWEEK'], errors='coerce')
                        dfactive24 =df24[df24['RWEEK']>=wk2] #still active within 2 weeks
                        
                        #LOST IN TWO WEEKS... REAL MISSED APPOINTMENT FOR THIS
                        df2wks =df24[df24['RWEEK']<wk2].copy()
                        two = df2wks.shape[0]
            
                        df3wks = df24[df24['RWEEK']<wk3]
                        three = df3wks.shape[0]
            
                        df4wks =df24[df24['RWEEK']<wk4]
                        four = df4wks.shape[0]
            
                        dfactive = pd.concat([dfactive24, df25]) #COMBINE THOSE ACTIVE IN TWO WEEKS AND THOSE OF 2025
                        curr = dfactive.shape[0]
        
                       #OF THOSE ACTIVE, HOW MANY WERE ON APPT 2 WEEKS AGO, 
                        dfactive['RWEEKR'] = pd.to_numeric(dfactive['RWEEKR'], errors='coerce')
                        appt = dfactive[dfactive['RWEEK']<wk2].copy()
                        onappt = appt.shape[0]
    
                        #MMD AMONGST ACTIVE CLIENTS
                        dfactive['ARVD'] = dfactive['ARVD'].fillna(20)
                        dfactive['ARVD'] = pd.to_numeric(dfactive['ARVD'], errors='coerce')
                        def mmd(a):
                            if a<90:
                                return '<3 MTHS'
                            elif a< 180:
                                return '<6 MTHS'
                            else:
                                return '6 MTHS+'
                        dfactive = dfactive.copy() #avoid fragmentation
                        dfactive['MULTI'] = dfactive['ARVD'].apply(mmd)
                        dfactive['MULTI'] = dfactive['MULTI'].astype(str)
                        df2mths =  dfactive[dfactive['MULTI']=='<3 MTHS'].copy()
                        M2 = df2mths.shape[0]
                        df3mths =  dfactive[dfactive['MULTI']=='<6 MTHS'].copy()
                        M3 = df3mths.shape[0]
                        df6mths =  dfactive[dfactive['MULTI']=='6 MTHS+'].copy()
                        M6 = df6mths.shape[0]
            
                        #VL SECTION
                        #REMOVING SIX MONTHS TX NEW, to take those that got ART in the Q
                        dfactive['Ayear'] = pd.to_numeric(dfactive['Ayear'], errors='coerce') 
                        VLa = dfactive[dfactive['Ayear']<2024].copy()
                        VLb = dfactive[dfactive['Ayear']==2024].copy()
                        VLb = VLb[VLb['Amonth']<7].copy()
                        VL = pd.concat([VLa,VLb])
                        el = VL.shape[0]
                        VL[['Vyear', 'Vmonth']] = VL[['Vyear', 'Vmonth']].apply(pd.to_numeric, errors='coerce')
                        WVL = VL[((VL['Vyear']>2023) | ((VL['Vyear']==2023) & (VL['Vmonth']>9)))].copy()
                        NVL = VL[((VL['Vyear']<2023) | ((VL['Vyear']==2023) & (VL['Vmonth']<10)))].copy()
                        nvl = NVL.shape[0]
                        wvl = WVL.shape[0]
            
                        #VL COV AMONG LOST CLIENTS
                        df2wks['Ayear'] = pd.to_numeric(df2wks['Ayear'], errors='coerce')
                        LVLa = df2wks[df2wks['Ayear']<2024].copy()
                        LVLb = df2wks[df2wks['Ayear']==2024].copy()
                        LVLb = LVLb[LVLb['Amonth']<7].copy()
                        LVL = pd.concat([LVLa,LVLb])
                        Lel = LVL.shape[0] #LOST ELIGIBLE
                        LVL[['Vyear', 'Vmonth']] = LVL[['Vyear', 'Vmonth']].apply(pd.to_numeric, errors='coerce')
                        LWVL = LVL[((LVL['Vyear']>2023) | ((LVL['Vyear']==2023) & (LVL['Vmonth']>9)))].copy()
                        LNVL = LVL[((LVL['Vyear']<2023) | ((LVL['Vyear']==2023) & (LVL['Vmonth']<10)))].copy()
                        lnvl = LNVL.shape[0]
                        lwvl = LWVL.shape[0]
                        totalvl = pd.concat([LNVL,NVL])
        
                        # #CIRA CUT OFF FOR A YEAR
                        # oneyear[['Ryear', 'Rmonth']] = oneyear[['Ryear', 'Rmonth']].apply(pd.to_numeric, errors = 'coerce')
                        # dfcira1 = oneyear[oneyear['Ryear']==2023].copy() #for 2023 ALTER
                        # dfcira2 = oneyear[oneyear['Ryear']==2024].copy() 
                        # dfcira1 = pd.to_numeric(dfcira1['Rmonth'], errors='coerce')
                        # dfcira1 = dfcira1[dfcira1['Rmonth']>9].copy()  #Cut off for 1 year 
        
                        # dfcira2[['Rday', 'Rmonth']] = dfcira2[['Rday', 'Rmonth']].apply(pd.to_numeric, errors = 'coerce')
                        # dfcira2 = dfcira2[((dfcira2['Rmonth'] <9) |((dfcira2['Rmonth'] ==9) & (dfcira2['Rday'] <3)))].copy()
    
                        # dfcira = pd.concat([dfcira1, dfcira2])
                        # dfcira['Tyear'] = pd.to_numeric(dfcira['Tyear'], errors='coerce')
                        # dfcira = dfcira[dfcira['Tyear']==994]
                        # dfcira['Dyear'] = pd.to_numeric(dfcira['Dyear'], errors='coerce')
                        # dfcira = dfcira[dfcira['Dyear']==994]
    
                        #EARLY RETENTION
                        #ONE YEAR COHORT
                        oneyear[['Ayear', 'Amonth']] = oneyear[['Ayear', 'Amonth']].apply(pd.to_numeric, errors = 'coerce')
                        new = oneyear[((oneyear['Ayear']==2023) & (oneyear['Amonth'].isin([10,11,12])))].copy()
                        newtotal = new.shape[0]
            
                        new[['Tiyear']] = new[['Tiyear']].apply(pd.to_numeric, errors = 'coerce')
                        tin = new[new['Tiyear']!=994].copy()
                        #one =new.shape[0]
                        newti = tin.shape[0]
                        orig = int(newtotal)-int(newti)
                        
                        new['Dyear'] = pd.to_numeric(new['Dyear'], errors='coerce')
                        newdead = new[new['Dyear']!=994].copy()
            
                        deadnew = newdead.shape[0]
                        new = new[new['Dyear']==994].copy() #AFTER REMOVING THE DEAD
            
                        new['Tyear'] = pd.to_numeric(new['Tyear'], errors='coerce')
                        
                        newto = new[new['Tyear']!=994].copy()
                        outnew = newto.shape[0]
                        
                        new = new[new['Tyear']==994].copy() #withou TO
                        netnew = new.shape[0]
            
                        new['A'] = pd.to_numeric(new['A'], errors = 'coerce')
                        dfactive['A'] = pd.to_numeric(dfactive['A'], errors = 'coerce')
                        
                        activen = new[new['A'].isin(dfactive['A'])].copy()
                        lostn = new[~new['A'].isin(dfactive['A'])].copy()           
            
                        newactive = activen.shape[0]
                        newlost = lostn.shape[0]
                        #st.write(newlost)
                        #VL SECTION AT ONE YEAR
                        activen[['Vyear', 'Vmonth']] = activen[['Vyear', 'Vmonth']].apply(pd.to_numeric, errors='coerce')
                        WVLa = activen[ ((activen['Vyear']==2024) & (activen['Vmonth']>9))].copy()
                        NVLa = activen[((activen['Vyear']<2024) | ((activen['Vyear']==2024) & (activen['Vmonth']<10)))].copy()
                        nvla = NVLa.shape[0]
                        wvla = WVLa.shape[0]
                                
                        #ret = newtotal - newlost
                        if netnew == 0:
                            rete = 0
                        elif newactive == 0:
                            rete = 0
                        else:
                            rete = round((newactive/netnew)*100)
                            #rete = f"{rete} %"
                        #9 MONTH COHORT
            
                        oneyear[['Ayear', 'Amonth']] = oneyear[['Ayear', 'Amonth']].apply(pd.to_numeric, errors = 'coerce')
                        new9 = oneyear[((oneyear['Ayear']==2024) & (oneyear['Amonth'].isin([1,2,3])))].copy()
                        newtotal9 = new9.shape[0]
            
                        new9[['Tiyear']] = new9[['Tiyear']].apply(pd.to_numeric, errors = 'coerce')
                        tin9 = new9[new9['Tiyear']!=994].copy()
                        #one =new.shape[0]
                        newti9 = tin9.shape[0]
                        orig9 = int(newtotal9)-int(newti9)
                        new9['Dyear'] = pd.to_numeric(new9['Dyear'], errors='coerce')
                        newdead9 = new9[new9['Dyear']!=994].copy()
            
                        deadnew9 = newdead9.shape[0]
                        new9 = new9[new9['Dyear']==994].copy() #AFTER REMOVING THE DEAD
            
                        new9['Tyear'] = pd.to_numeric(new9['Tyear'], errors='coerce')
                        
                        newto9 = new9[new9['Tyear']!=994].copy()
                        outnew9 = newto9.shape[0]
                        
                        new9 = new9[new9['Tyear']==994].copy() #withou TO
                        netnew9 = new9.shape[0]
            
                        new9['A'] = pd.to_numeric(new9['A'], errors = 'coerce')
                        dfactive['A'] = pd.to_numeric(dfactive['A'], errors = 'coerce')
                        
                        active9 = new9[new9['A'].isin(dfactive['A'])].copy()
                        lostn9 = new9[~new9['A'].isin(dfactive['A'])].copy()
                    
                        newactive9 = active9.shape[0]
                        newlost9 = lostn9.shape[0]
                        #ret = newtotal - newlost
                        if netnew9 == 0:
                            rete9 = 0
                        elif newactive9 == 0:
                            rete9 = 0
                        else:
                            rete9 = round((newactive9/netnew9)*100)
                    
                    
            
                    #6 MONTH COHORT
            
                        oneyear[['Ayear', 'Amonth']] = oneyear[['Ayear', 'Amonth']].apply(pd.to_numeric, errors = 'coerce')
                        new6 = oneyear[((oneyear['Ayear']==2024) & (oneyear['Amonth'].isin([4,5,6])))].copy()
                        newtotal6 = new6.shape[0]
            
                        new6[['Tiyear']] = new6[['Tiyear']].apply(pd.to_numeric, errors = 'coerce')
                        tin6 = new6[new6['Tiyear']!=994].copy()
                        #one =new.shape[0]
                        newti6 = tin6.shape[0]
                        orig6 = int(newtotal6)-int(newti6)
                        new6['Dyear'] = pd.to_numeric(new6['Dyear'], errors='coerce')
                        newdead6 = new6[new6['Dyear']!=994].copy()
            
                        deadnew6 = newdead6.shape[0]
                        new6 = new6[new6['Dyear']==994].copy() #AFTER REMOVING THE DEAD
            
                        new6['Tyear'] = pd.to_numeric(new6['Tyear'], errors='coerce')
                        
                        newto6 = new6[new6['Tyear']!=994].copy()
                        outnew6 = newto6.shape[0]
                        
                        new6 = new6[new6['Tyear']==994].copy() #withou TO
                        netnew6 = new6.shape[0]
            
                        new6['A'] = pd.to_numeric(new6['A'], errors = 'coerce')
                        dfactive['A'] = pd.to_numeric(dfactive['A'], errors = 'coerce')
                        
                        active6 = new6[new6['A'].isin(dfactive['A'])].copy()
                        lostn6 = new6[~new6['A'].isin(dfactive['A'])].copy()
                    
                        newactive6 = active6.shape[0]
                        newlost6 = lostn6.shape[0]
                        #st.write(newlost)
                        #VL SECTION AT 6 MONTHS
                        active6[['Vyear', 'Vmonth']] = active6[['Vyear', 'Vmonth']].apply(pd.to_numeric, errors='coerce')
                        WVLa6 = active6[active6['Vyear']==2024].copy()
                        NVLa6 = active6[active6['Vyear']!=2024].copy()
                        nvla6 = NVLa6.shape[0]
                        wvla6 = WVLa6.shape[0]
                        #ret = newtotal - newlost
                        if netnew6 == 0:
                            rete6 = 0
                        elif newactive6 == 0:
                            rete6 = 0
                        else:
                            rete6 = round((newactive6/netnew6)*100)
                            #rete6 = f"{rete6} %"
            
                    #3 MONTH COHORT
            
                        oneyear[['Ayear', 'Amonth']] = oneyear[['Ayear', 'Amonth']].apply(pd.to_numeric, errors = 'coerce')
                        new3 = oneyear[((oneyear['Ayear']==2024) & (oneyear['Amonth'].isin([7,8,9])))].copy()
                        newtotal3 = new3.shape[0]
            
                        new3[['Tiyear']] = new3[['Tiyear']].apply(pd.to_numeric, errors = 'coerce')
                        tin3 = new3[new3['Tiyear']!=994].copy()
                        #one =new.shape[0]
                        newti3 = tin3.shape[0]
                        orig3 = int(newtotal3)-int(newti3)
                        
                        new3['Dyear'] = pd.to_numeric(new3['Dyear'], errors='coerce')
                        newdead3 = new3[new3['Dyear']!=994].copy()
            
                        deadnew3 = newdead3.shape[0]
                        new3 = new3[new3['Dyear']==994].copy() #AFTER REMOVING THE DEAD
            
                        new3['Tyear'] = pd.to_numeric(new3['Tyear'], errors='coerce')
                        
                        newto3 = new3[new3['Tyear']!=994].copy()
                        outnew3 = newto3.shape[0]
                        
                        new3 = new3[new3['Tyear']==994].copy() #withou TO
                        netnew3 = new3.shape[0]
            
                        new3['A'] = pd.to_numeric(new3['A'], errors = 'coerce')
                        dfactive['A'] = pd.to_numeric(dfactive['A'], errors = 'coerce')
                        
                        active3 = new3[new3['A'].isin(dfactive['A'])].copy()
                        lostn3 = new3[~new3['A'].isin(dfactive['A'])].copy()
                        
            
                        newactive3 = active3.shape[0]
                        newlost3 = lostn3.shape[0]
                        #st.write(newlost)
                                
                        #ret = newtotal - newlost
                        if netnew3 == 0:
                            rete3 = 0
                        elif newactive3 == 0:
                            rete3 = 0
                        else:
                            rete3 = round((newactive3/netnew3)*100)
                            #rete3 = f"{rete3} %"
            
                        oneyear[['Ayear', 'Amonth']] = oneyear[['Ayear', 'Amonth']].apply(pd.to_numeric, errors = 'coerce')
                        new1 = oneyear[((oneyear['Ayear']==2024) & (oneyear['Amonth'].isin([10,11,12])))].copy()
                        newtotal1 = new1.shape[0]
            
                        new1[['Tiyear']] = new1[['Tiyear']].apply(pd.to_numeric, errors = 'coerce')
                        tin1 = new1[new1['Tiyear']!=994].copy()
                        #one =new.shape[0]
                        newti1 = tin1.shape[0]
                        orig1 = int(newtotal1)-int(newti1)
                        
                        new1['Dyear'] = pd.to_numeric(new1['Dyear'], errors='coerce')
                        newdead1 = new1[new1['Dyear']!=994].copy()
            
                        deadnew1 = newdead1.shape[0]
                        new1 = new1[new1['Dyear']==994].copy() #AFTER REMOVING THE DEAD
            
                        new1['Tyear'] = pd.to_numeric(new1['Tyear'], errors='coerce')
                        
                        newto1 = new1[new1['Tyear']!=994].copy()
                        outnew1 = newto1.shape[0]
                        
                        new1 = new1[new1['Tyear']==994].copy() #withou TO
                        netnew1 = new1.shape[0]
            
                        new1['A'] = pd.to_numeric(new1['A'], errors = 'coerce')
                        dfactive['A'] = pd.to_numeric(dfactive['A'], errors = 'coerce')
                        
                        active1 = new1[new1['A'].isin(dfactive['A'])].copy()
                        lostn1 = new1[~new1['A'].isin(dfactive['A'])].copy()    
            
                        newactive1 = active1.shape[0]
                        newlost1 = lostn1.shape[0]
                        #st.write(newlost)
                                
                        #ret = newtotal - newlost
                        if netnew1 == 0:
                            rete1 = 0
                        elif newactive1 == 0:
                            rete1 = 0
                        else:
                            rete1 = round((newactive1/netnew1)*100)
                            #rete1 = f"{rete1} %"
                        # if st.session_state.reader:
                        #     st.write(pot)
                        list1 = [lastq,pot,ti,txnew,rtt,true,dead,two,three,four,curr,M2,M3,M6, onappt ] #TX
                        
                        list2 = [curr,el,wvl,nvl,two,Lel, lnvl,lwvl, newactive,wvla,nvla,newactive6,wvla6,nvla6] #VL
                        
                        list3 = [newtotal, orig,newti,deadnew,outnew, newlost,netnew,newactive,rete,
                                     newtotal6, orig6,newti6,deadnew6,outnew6,newlost6,netnew6, newactive6,rete6,
                                  newtotal9, orig9,newti9,deadnew9,outnew9,newlost9,netnew9, newactive9,rete9] #YEAR
                        list4 = [newtotal3, orig3,newti3,deadnew3,outnew3,newlost3,netnew3, 
                                     newactive3,rete3,newtotal1, orig1,newti1,deadnew1,outnew1,newlost1,netnew1, newactive1,rete1] #THRRE
                        # st.session_state.reader =True
                        lst = df2wks[['A', 'RD']].copy()
                        tout = dft[['A', 'TO']].copy()
                        die = died[['A', 'DD']].copy()
                        vir = totalvl[['A', 'VD']].copy()
                        one = lostn[['A','AS','RD']].copy()
                    
                        lst['MISSED'] = np.nan
                        lst['MISSED'] = lst['MISSED'].fillna('MISSED APPT')
                        lst['A'] = pd.to_numeric(lst['A'], errors='coerce')
                    
                        tout['TRANSFERED'] = np.nan
                        tout['TRANSFERED'] = tout['TRANSFERED'].fillna('TO')
                        first = pd.concat([lst,tout])#, on = 'A', how = 'outer')
                    
                        die['DEAD?'] = np.nan
                        die['DEAD?'] = die['DEAD?'].fillna('DIED')
                        second = pd.concat([first,die])#, on = 'A', how = 'outer')
                        
                        vir['VL STATUS'] = np.nan
                        vir['VL STATUS'] = vir['VL STATUS'].fillna('DUE')
                        vir['A'] = pd.to_numeric(vir['A'], errors='coerce')
                        second['A'] = pd.to_numeric(second['A'], errors='coerce')
                        third = pd.merge(second,vir, on = 'A', how = 'outer')
                    
                        one['ONE YEAR'] = np.nan
                        one['ONE YEAR'] = one['ONE YEAR'].fillna('ONE YEAR IIT')
                        forth = pd.concat([third,one])#, on = 'A', how = 'outer')
                            
    if st.session_state.reader:                                                    
        file2 = r'CLUSTERS.csv'
        dfx = pd.read_csv(file2)
        clusters  = list(dfx['CLUSTER'].unique())
        cluster = st.radio(label='**Choose your cluster**', options=clusters,index=None, horizontal=True)
        if not cluster:
            st.stop()
        else:
            districts = dfx[dfx['CLUSTER']==cluster]
            districts = list(districts['DISTRICT'].unique())
            district = st.radio(label='**Choose your district**', options=districts,index=None, horizontal=True)
            if not district:
                st.stop()
            else:
                facilities = dfx[dfx['DISTRICT']==district]
                facilities = facilities['FACILITY'].unique()
                facility = st.selectbox(label='**Choose your facility**', options=facilities,index=None)
                if not facility:
                    st.stop()
                else:
                    # st.write(facility)
                    pass
    if st.session_state.reader:# and st.session_state.df:
                    @st.cache_data
                    def lastqtr():
                        dat = last.copy()
                        dat = dat[['ART', 'RD']].copy()
                        dat = dat.rename(columns ={'ART':'ART NO.', 'RD':'RETURN DATE'})
                        return dat
                    @st.cache_data
                    def lost():
                        dat = df2wks.copy()
                        dat = dat[['ART', 'RD']].copy()
                        dat = dat.rename(columns ={'ART':'ART NO.', 'RD':'RETURN DATE'})
                        return dat
                    @st.cache_data
                    def transfer():
                        dat = dft.copy()
                        dat = dat[['ART', 'RD', 'TO']]
                        dat = dat.rename(columns ={'ART':'ART NO.', 'RD':'RETURN DATE', 'TO':'TRANSFER OUT DATE'})
                        return dat
                    @st.cache_data
                    def deceased():
                        dat = died.copy()
                        dat = dat[['ART', 'RD', 'DD']].copy()
                        dat = dat.rename(columns ={'ART':'ART NO.', 'RD':'RETURN DATE', 'DD':'DEATH DATE'})
                        return dat
                    @st.cache_data
                    def viral():
                        dat = totalvl.copy()
                        dat = dat[['ART', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    ####ONE YEAR
                    @st.cache_data
                    def yearto():
                        dat = newto.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearlost():
                        dat = lostn.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.', 'AS':'ART START DATE','RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearvl():
                        dat = NVLa.copy()
                        dat = dat[['ART', 'AS','RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    ####6 MONTHS
                    @st.cache_data
                    def yearto6():
                        dat = newto6.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearlost6():
                        dat = lostn6.copy()
                        dat = dat[['ART', 'AS','RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearvl6():
                        dat = NVLa6.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.', 'AS':'ART START DATE','RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    ####3 MONTHS
                    @st.cache_data
                    def yearto3():
                        dat = newto3.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearlost3():
                        dat = lostn3.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearto3():
                        dat = newto3.copy()
                        dat = dat[['ART', 'AS','RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearlost3():
                        dat = lostn3.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearto1():
                        dat = newto1.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat
                    @st.cache_data
                    def yearlost1():
                        dat = lostn1.copy()
                        dat = dat[['ART','AS', 'RD', 'VD']]
                        dat = dat.rename(columns ={'ART':'ART NO.','AS':'ART START DATE', 'RD':'RETURN DATE', 'VD':'VIRAL LOAD DATE'})
                        return dat                  
                    preva = dfx[dfx['FACILITY']==facility] 
                    prev = preva['Q4 CUR'].sum()
                    #prev = int(preva.iloc[0,4])
                    #UK = pot- prev #- inn - newad
                    #dd = dead.shape[0]
                    # if UK <0:
                    #     st.warning('THIS EXTRACT HAS LESS CLIENTS THAN EVER ENROLLED AT THE FACILITY')
                    #     st.stop()
                    # else:
                    #     pass
                    part = [cluster,district,facility,week,wk,prev]
                    #ADDING THE CLUSTER PART
    
                    row1 = part + list1
                
                    row2 = part + list2
                
                    row3 = part + list3
                
                    row4 = part + list4
                    col1,col2,col3 = st.columns([1,2,1])
                    with col3:
                        submit = st.button('Submit') 
                    
                    secrets = st.secrets["connections"]["gsheets"]
                    
                        # Prepare the credentials dictionary
                    credentials_info = {
                            "type": secrets["type"],
                            "project_id": secrets["project_id"],
                            "private_key_id": secrets["private_key_id"],
                            "private_key": secrets["private_key"],
                            "client_email": secrets["client_email"],
                            "client_id": secrets["client_id"],
                            "auth_uri": secrets["auth_uri"],
                            "token_uri": secrets["token_uri"],
                            "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
                            "client_x509_cert_url": secrets["client_x509_cert_url"]
                        }
                            
                    try:
                        # Define the scopes needed for your application
                        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                                "https://www.googleapis.com/auth/drive"]
                        
                         
                        credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
                            
                            # Authorize and access Google Sheets
                        client = gspread.authorize(credentials)
                            
                            # Open the Google Sheet by URL
                        spreadsheetu = "https://docs.google.com/spreadsheets/d/1twNlv9MNQWWsM73_dA19juHkp_Hua-k-fJA1qNVwQl0"
                        spreadsheet = client.open_by_url(spreadsheetu)
                    except Exception as e:
                            # Log the error message
                        st.write(f"CHECK: {e}")
                        st.write(traceback.format_exc())
                        st.write("COULDN'T CONNECT TO GOOGLE SHEET, TRY AGAIN")
                        st.stop()
                    
                    if submit:
                            #st.write(row1)
                            try:
                                sheet1 = spreadsheet.worksheet("TX")
                                sheet1.append_row(row1, value_input_option='RAW')
                                
                                sheet2 = spreadsheet.worksheet("VL")
                                sheet2.append_row(row2, value_input_option='RAW')
                                
                                sheet3 = spreadsheet.worksheet("YEARS")
                                sheet4 = spreadsheet.worksheet("THREEO")
                                sheet3.append_row(row3, value_input_option='RAW')
                                sheet4.append_row(row4, value_input_option='RAW')
                                st.session_state.submited = True
                            except Exception as e:
                                # Print the error message
                                st.write(f"ERROR: {e}")
                                st.stop()  # Stop the Streamlit app here to let the user manually retry     
                    else:
                            st.write('FIRST SUBMIT TO SEE LINELISTS AND SUMMARY') 
                            st.markdown(f'**YOU HAVE SELECTED {district} AS THE DISTRICT AND {facility} AS THE FACILITY**')
                            st.write('BE SURE OF THE ABOVE SELECTIONS BEFORE SUBMITTING')                     
                    
                    if st.session_state.submited:
                            st.success('**SUBMITTED, To upload another excel, first refresh this page, or open the link afresh**')
                            #st.info('To upload another excel, first refresh this page, or open the link afresh')
                            st.divider()
                            st.write(f"<h6><b>DOWNLOAD LINELISTS FROM HERE</b></h6>", unsafe_allow_html=True)
                            cola, colb, colc = st.columns(3)
                            with cola:
                                    if two==0:
                                        st.write('**NO MISSED APPOINTMENTS**')
                                    else:
                                        dat = lost()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(
                                                    label="MISSED APPOINTMENTS",
                                                    data=csv_data,
                                                    file_name=f"{facility} MISSED.csv",
                                                    mime="text/csv")
                            with colb:
                                    if dead ==0:
                                        st.write('**NO DEAD CLIENTS**')
                                    else:
                                        dat = deceased()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(
                                                        label=" DEAD",
                                                        data=csv_data,
                                                        file_name=f" {facility} DEAD.csv",
                                                        mime="text/csv")
                            with colc:
                                    if true == 0:
                                        st.markdown('**NO TRANSFER OUTs**')
                                    else:
                                        dat = transfer()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(
                                                    label=" TRANSFER OUTS",
                                                    data=csv_data,
                                                    file_name=f" {facility} TOS.csv",
                                                    mime="text/csv")
                        ######################################VL SECTION
                            st.divider()
                            st.markdown("**LAST QUARTER'S TXML AND VIRAL LOAD LINE LIST**")
                            cola, colb = st.columns(2)
                            with cola:
                                dat = lastqtr()
                                csv_data = dat.to_csv(index=False)
                                st.download_button(
                                            label="TXML FOR LAST QTR",
                                            data=csv_data,
                                            file_name=f"{facility} LASTQtr.csv",
                                            mime="text/csv")
                            with colb:
                                dat = viral()
                                csv_data = dat.to_csv(index=False)
                                st.download_button(
                                            label="CURRENT VL LINELIST",
                                            data=csv_data,
                                            file_name=f"{facility} VL.csv",
                                            mime="text/csv")              
                            
                        #     #########################################################################################################################################################
                        ###ONE YEAR LINE LISTS
                            if st.session_state.submited: 
                                st.divider()
                                st.write(f"<h6><b>ONE YEAR COHORT LINELISTS </b></h6>", unsafe_allow_html=True)
                                cola, colb, colc = st.columns(3)
                                with cola:
                                        if newlost==0:
                                            st.write('**NO 1 YR IIT**')
                                        else:
                                            dat = yearlost()
                                            csv_data = dat.to_csv(index=False)
                                            st.download_button(key='a',
                                                        label="ONE YR IIT",
                                                        data=csv_data,
                                                        file_name=f"{facility} 1YR_IIT.csv",
                                                        mime="text/csv")
                                with colb:
                                        if outnew==0:
                                            st.markdown('**NO 1 YR TOs**')
                                        dat = yearto()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(key='b',
                                                    label=" 1 YR T.OUTS",
                                                    data=csv_data,
                                                    file_name=f" {facility} TO_1YR.csv",
                                                    mime="text/csv")
                                with colc:
                                    if nvla ==0:
                                        st.write('**NO ONE YEAR VL LIST**')
                                    else:
                                        dat = yearvl()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(key='c',
                                                    label="1 YR VL LINELIST",
                                                    data=csv_data,
                                                    file_name=f"{facility} VL_1YR.csv",
                                                    mime="text/csv")
                                
                            ###SIX YEAR LINE LISTS
                                st.divider() 
                                st.write(f"<h6><b>SIX MONTHS COHORT LINELISTS </b></h6>", unsafe_allow_html=True)
                                cola, colb, colc = st.columns(3)
                                with cola:
                                        if newlost6==0:
                                            st.write('**NO 6 MTHS IIT**')
                                        else:
                                            dat = yearlost6()
                                            csv_data = dat.to_csv(index=False)
                                            st.download_button(key='d',
                                                        label="SIX MTHS IIT",
                                                        data=csv_data,
                                                        file_name=f"{facility} IIT_6.csv",
                                                        mime="text/csv")
                                with colb:
                                        if outnew6==0:
                                            st.markdown('**NO 6 MTHS TOs**')
                                        dat = yearto6()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(key='e',
                                                    label=" 6 MTHS T.OUTS",
                                                    data=csv_data,
                                                    file_name=f" {facility} TO_1YR.csv",
                                                    mime="text/csv")
                                with colc:
                                    if nvla6 ==0:
                                        st.markdown('**NO 6 MTHS VL LIST**')
                                    else:
                                        dat = yearvl6()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(key='f',
                                                    label="6 MTHS VL",
                                                    data=csv_data,
                                                    file_name=f"{facility} VL6.csv",
                                                    mime="text/csv")
                                                            
                            ###THREE MTHS LINE LISTS
                                st.divider()
                                st.write(f"<h6><b>THREE MONTHS COHORT LINELISTS </b></h6>", unsafe_allow_html=True)
                                cola, colb = st.columns(2)
                                with cola:
                                        if newlost3==0:
                                            st.write('**NO 3 MTHS IIT**')
                                        else:
                                            dat = yearlost3()
                                            csv_data = dat.to_csv(index=False)
                                            st.download_button(key='g',
                                                        label="3 MTHS IIT",
                                                        data=csv_data,
                                                        file_name=f"{facility} IIT_3.csv",
                                                        mime="text/csv")
                                with colb:
                                        if outnew3==0:
                                            st.markdown('**NO 3 MTHS TOs**')
                                        dat = yearto3()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(key='h',
                                                    label="3 MTHS T.OUTS",
                                                    data=csv_data,
                                                    file_name=f" {facility} TOs_3.csv",
                                                    mime="text/csv")                    
                            
                            ###THREE MTHS LINE LISTS   
                                st.divider()
                                st.write(f"<h6><b>TX NEW LINELISTS </b></h6>", unsafe_allow_html=True)
                                cola, colb = st.columns(2)
                                with cola:
                                        if newlost1==0:
                                            st.write('**NO TX NEW IIT**')
                                        else:
                                            dat = yearlost1()
                                            csv_data = dat.to_csv(index=False)
                                            st.download_button(key='j',
                                                        label="TX NEW IIT",
                                                        data=csv_data,
                                                        file_name=f"{facility} IIT_NEW.csv",
                                                        mime="text/csv")
                                with colb:
                                    if outnew1==0:
                                            st.markdown('**NO TxNEW TOs**')
                                    else:
                                        dat = yearto1()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(key='k',
                                                    label="TXNEW T.OUTS",
                                                    data=csv_data,
                                                    file_name=f" {facility} TxNEW_TOs.csv",
                                                    mime="text/csv") 
                                st.divider()
                                forth = forth.rename(columns = {'A': 'ART NO.','VD': 'VL DATE', 'RD': 'RETURN DATE', 'DD': 'DEATH DATE', 'TO': 'TRANSFER OUT DATE', 'AS': 'ART START DATE'})
                                cola,colb = st.columns([4,1])
                                with cola:
                                        if outnew1==0:
                                            st.markdown('**MASTER LIST WITH ALL LINELISTS COMBINED**')
                                        dat = forth.copy()
                                        #dat = rt.copy()
                                        csv_data = dat.to_csv(index=False)
                                        st.download_button(
                                                    label="MASTER_LIST",
                                                    data=csv_data,
                                                    file_name=f" {facility} MASTER_LIST.csv",
                                                    mime="text/csv")
                
                                st.divider()
                                st.write(FYB)
                                st.success('**WANT TO HELP US IMPROVE?**')
                                st.write('Are you getting different results when you filter the extract manually?, That is ok')
                                st.write('**The intention of this program is to get the same results as you would manually, so help us improve by sending any variation you get to the TWG**')
                                st.warning('Refer to the SOP section to see how this program arrives to the summaries and linelists you are seeing')
                                st.write('')
                                st.write('')
                                st.write('')
                                st.success('**CREATED BY Dr. LUMINSA DESIRE**')
                                st.info('**WITH CONTRIBUTION FROM EDISON KATUNGUKA, SIMON SEMAKULA AND CHRIS MUGARA, FOR THE TWG**')
pages = {
    "READER:": [
        st.Page(extract, title="EMR EXTRACT READER"),
    ],
    "VISUALISATION:":[
        st.Page("RETENTION.py", title="RETENTION"),
        st.Page("VL_SECTION.py", title="VIRAL LOAD")],
    "RESOURCES:": [
        st.Page("SOPs.py", title="SOPs"),
        st.Page("USER_MANUAL.py", title="USER MANUAL"),
    ],
}

pg = st.navigation(pages)
pg.run()
                                
    
