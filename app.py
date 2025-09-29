import streamlit as st
import pandas as pd
import numpy as np


# Título da pagina
st.title("Uber pickups in NYC")


# Variaveis
DATA_COLUMN = 'date/time'
DATE_URL = ("https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/main/uber-raw-data-sep14.csv.gz")


# Função para carregar os dados
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATE_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower() # Converter nomes das colunas para minusculas
    data.rename(lowercase, axis='columns', inplace=True) # Renomear colunas
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN]) # Converter coluna de data/hora para formato datetime
    return data


# Chama a Função para carregar os dados
data_load_state = st.text('Loading data...') # Mensagem de carregamento
data = load_data(10000)
data_load_state.text("") 


# Cliente ver os dados brutos
if st.checkbox('Show raw data'): # Checkbox para mostrar os dados brutos
    st.subheader('Raw data') # Subtitulo
    st.write(data) # Mostrar os dados brutos


# Histograma dos pickups por hora
st.subheader('Number of pickups by hour') # Subtitulo
hist_values = np.histogram(data[DATA_COLUMN].dt.hour, bins=24, range=(0,24))[0] # Calcular histograma
st.bar_chart(hist_values) # Mostrar histograma como gráfico de barras   


# Filtrar dataset 
hour_to_filter = st.slider('hour', 0, 23, 17) # Slider 
filtered_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter] # Filtrar dados pela hora selecionada


# Mostrar mapa com localização dos embarques
st.subheader(f'Map of all pickups at {hour_to_filter}:00') # Subtitulo
st.map(filtered_data) # Mostrar mapa com os dados filtrados