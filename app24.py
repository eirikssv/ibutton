import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from io import StringIO
import minstil 
st.set_page_config(layout='wide')

@st.cache_data
def convert_df(df):
    return df.to_csv(sep=";", decimal=",", index=False).encode('utf-8')

df = None

st.header('iButton-parser')
st.markdown('''
Hensikten med denne appen er å hente over data fra iButton og automagisk utføre re-formateringen som ofte må til. 

* For å bruke: Kopier data fra iButton via ibuttonviewer.jar; velg mission, høyreklikk og velg "Copy data with labels".
* Lim data inn i tekstområdet nedenfor.
* Verifiser at ting ser ok ut.
* Lagre som .csv

''')

# Text area for user to paste the clipboard content
data_input = st.text_area("Lim data her", height=200)

# Process the data when content is pasted into the text area
if data_input:
    df = pd.read_csv(StringIO(data_input), sep=";", header=None)
    df.columns = ['Raw']
    df['Datetime'] = df['Raw'].str[:17]
    df['Datetime'] = pd.to_datetime(df['Datetime'], dayfirst=True)
    df['Temp'] = df['Raw'].str[20:]
    df['Temp'] = df['Temp'].str.replace(",", ".")
    df['Temp'] = df['Temp'].astype(float)
    df.drop('Raw', inplace=True, axis=1)

if df is not None:
    form_csv = convert_df(df)
    st.download_button('Lagre .csv', data=form_csv, file_name='Nedlastning.csv')

    last_date = df['Datetime'].iloc[-1]
    first_date = df['Datetime'].iloc[0]
    difference = (last_date - first_date)
    cdays1 = round(difference.total_seconds()/3600/24, 2)
    cdays2 = f"{cdays1} dager med data"
    sample2 = df['Datetime'].iloc[1]
    sample1 = df['Datetime'].iloc[0]
    difference = (sample2 - sample1)
    sample_rate = f"{difference.total_seconds()}s sample rate"
    df2 = df.sort_values(by='Temp', ascending=True)
    df2.drop_duplicates(subset=['Temp'], inplace=True)
    smallest = df2.nsmallest(2, 'Temp')['Temp'].iloc[0]
    smallest2 = df2.nsmallest(2, 'Temp')['Temp'].iloc[1]
    temp_diff = f"{smallest2 - smallest}°C logging accuracy"
    
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    
    fig = px.line(df, x='Datetime', y='Temp', width=1200, title=f'{cdays2}, {sample_rate}, {temp_diff}', template='sintef')

    st.plotly_chart(fig)
    col1, col2, col3 = st.columns(3)
    col1.header('Dataframe')
    col1.dataframe(df)
    col2.header('df.info()')
    col2.text(s)
    col3.header('df.describe()')
    col3.text(df.describe())
