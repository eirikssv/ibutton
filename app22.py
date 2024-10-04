import pandas as pd, numpy as np, plotly.express as px
import streamlit as st
st.set_page_config(layout='wide')
from io import StringIO, BytesIO
import base64
import minstil
@st.cache
def convert_df(df):
    return df.to_csv(sep=";", decimal=",", index=False).encode('utf-8')

df = None

st.header('iButton-parser')
st.markdown('''
Hensikten med denne appen er å hente over data fra iButton og automagisk utføre re-formateringen som ofte må til. 

* For å bruke: Kopier data fra iButton via ibuttonviewer.jar; velg mission, høyreklikk og velg "Copy data with labels".
* Trykk på Les clipboard
* Verifiser at ting ser ok ut
* Lagre som .csv

''')

read_clip = st.button("Les clipboard")
if read_clip:
    df = pd.read_clipboard(sep=";", header=None)
    df.columns = ['Raw']
    df['Datetime'] = df['Raw'].str[:17]
    df['Datetime'] = pd.to_datetime(df['Datetime'], dayfirst=True)
    df['Temp'] = df['Raw'].str[20:]
    df['Temp'] = df['Temp'].str.replace(",",".")
    df['Temp'] = df['Temp'].astype(float)
    df.drop('Raw', inplace=True, axis=1)

if df is not None:
    form_csv = convert_df(df)
    st.download_button('Lagre .csv', data=form_csv, file_name='Nedlastning.csv')

    last_date = df['Datetime'].iloc[-1]
    first_date = df['Datetime'].iloc[0]
    difference = (last_date - first_date)
    cdays1 = round(difference.total_seconds()/3600/24, 2)
    cdays = str(difference.total_seconds()/3600/24)[0:2] + str(' dager med data')
    cdays2 = str(cdays1) + str(' dager med data')
    sample2 = df['Datetime'].iloc[1]
    sample1 = df['Datetime'].iloc[0]
    difference = (sample2 - sample1)
    sample_rate = str(difference.total_seconds()) + str('s sample rate')
    df2 = df.sort_values(by='Temp', ascending=True)
    df2.drop_duplicates(subset=['Temp'], inplace=True)
    smallest = df2.nsmallest(2, 'Temp')['Temp'].iloc[0]
    smallest2 = df2.nsmallest(2, 'Temp')['Temp'].iloc[1]
    temp_diff = smallest2 - smallest
    temp_diff = str(temp_diff) + str('°C logging accuracy')
    
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