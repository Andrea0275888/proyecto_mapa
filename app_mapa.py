import pandas as pd
import streamlit as st
import pydeck as pdk
import chardet 
import time

st.title("Mapa del tráfico en Guadalajara")

with open("dataset2024.csv", "rb") as f:
    result = chardet.detect(f.read(100000))

encoding_detectada= result["encoding"]

df = pd.read_csv("dataset2024.csv", encoding=encoding_detectada)

df["Coordx"]=pd.to_numeric(df["Coordx"], errors="coerce")
df["Coordy"] = pd.to_numeric(df["Coordy"], errors="coerce")

df = df.dropna(subset=["Coordx", "Coordy"])

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df= df.dropna(subset=["timestamp"])



df["hour"] = df["timestamp"].dt.floor("h")
df = df.sort_values(by="timestamp")
horas_sorted= sorted(df["hour"].unique())

COLOR_MAP={
    "green": [0,255,0], 
    "red": [255,0,0],
    "red_wine":[128,0,32], 
    "orange": [255,165,0]
}

df["color"]= df["predominant_color"].map(COLOR_MAP)

map_placeholder=st.empty()

for hour in horas_sorted: 
    batch_actual= df[df["hour"]== hour]
    st.write("Hora: ", hour)
    
    layer= pdk.Layer(
        "ScatterplotLayer",
        data= batch_actual, 
        get_position=["Coordx", "Coordy"],
        get_radius = 400,
        get_color="color",
        pickable= True,
    )

    view_state= pdk.ViewState(
        latitude= df["Coordy"].mean(),
        longitude=df["Coordx"].mean(),
        zoom=11,
    ) 
    
    mapa = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    )

    map_placeholder.pydeck_chart(mapa)

    time.sleep(1)