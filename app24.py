import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from io import StringIO
import minstil 
import humanize
from datetime import datetime
st.set_page_config(layout='wide')

@st.cache_data
def convert_df(df):
    return df.to_csv(sep=";", decimal=",", index=False).encode('utf-8')

df = None


st.header('iButton-parser')
col1, col2 = st.columns([2, 1])

col1.markdown('''
Hensikten med denne appen er å hente over data fra iButton og automagisk utføre re-formateringen som ofte må til. 

* For å bruke: Kopier data fra iButton via ibuttonviewer.jar; velg mission, høyreklikk og velg "Copy data with labels".
* Lim data inn i tekstområdet nedenfor.
* Verifiser at ting ser ok ut.
* Lagre som .csv

''')

# Text area for user to paste the clipboard content
data_input = col2.text_area("Lim data her", height=200)

def norwegian_humanize(seconds):
    duration = humanize.naturaldelta(seconds)
    translations = {
        'days': 'dager',
        'hours': 'timer',
        'minutes': 'minutter',
        'weeks': 'uker',
        'months': 'måneder',
        'years': 'år',
        'day': 'dag',
        'hour': 'time',
        'minute': 'minutt',
        'week': 'uke',
        'month': 'måned',
        'year': 'år',
        'seconds': 'sekunder',
        'second': 'sekund'
    }
    for eng, nor in translations.items():
        duration = duration.replace(eng, nor)
    return duration


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
    date_today = datetime.today().strftime('%Y-%m-%d')
    st.download_button('Last ned formatert data (.csv)', data=form_csv, file_name=f'iButton_data_{date_today}.csv')

    # Beregne loggeperioden
    last_date = df['Datetime'].iloc[-1]
    first_date = df['Datetime'].iloc[0]
    difference = (last_date - first_date)
    periode = norwegian_humanize(difference.total_seconds())

    # Sample rate
    sample2 = df['Datetime'].iloc[1]
    sample1 = df['Datetime'].iloc[0]
    difference = (sample2 - sample1)
    sample_rate = norwegian_humanize(difference.total_seconds())

    # Oppløsning/resolution
    df2 = df.sort_values(by='Temp', ascending=True)
    df2.drop_duplicates(subset=['Temp'], inplace=True)
    smallest = df2.nsmallest(2, 'Temp')['Temp'].iloc[0]
    smallest2 = df2.nsmallest(2, 'Temp')['Temp'].iloc[1]
    temp_diff = smallest2 - smallest
    temp_diff = 0.5 if abs(temp_diff - 0.5) < abs(temp_diff - 0.0625) else 0.0625

    
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    
    col1, col2, col3 = st.columns(3)
    col1.metric('Loggeperiode', periode)
    col2.metric('Sample rate', sample_rate)
    col3.metric('Oppløsning', f'{temp_diff}°C')
    fig = px.line(df, x='Datetime', y='Temp', width=1200, template='sintef')

    st.plotly_chart(fig)
    col1, col2, col3 = st.columns(3)
    col1.header('Dataframe')
    col1.dataframe(df)
    col2.header('df.info()')
    col2.text(s)
    col3.header('df.describe()')
    col3.text(df.describe())
