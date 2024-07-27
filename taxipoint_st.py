import streamlit as st
import taxipoint
from sqlalchemy import create_engine
import time
import os

import plotly.io as pio
from PIL import Image

# # #
os.environ['TZ'] = 'Europe/Helsinki'
# time.tzset()

db_str = st.secrets["db_str"]
sql_engine = create_engine(db_str)

# # #

st.markdown(
        f"""
<style>
    .appview-container .main .block-container{{
        max-width: {2000}px;
        padding-left: {2}rem;
        paddint-right: {2}rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    "<h2 style='text-align: center; color: black;'>Helsinki-Vantaa -lentoasema <br>Taksikysynnän ennuste</h2>", 
    unsafe_allow_html=True
)

container = st.empty()
container2 = st.empty()

###
image = Image.open("plot.png")
scale = 0.2
w = int(3500 * scale)
h = int(1500 * scale)
image = image.resize((w,h))
loading_image = image.convert("RGBA")
data = image.getdata()
new_data = []
for item in data:
    new_data.append((item[0], item[1], item[2], 128))
loading_image.putdata(new_data)
###

with st.spinner("Loading..."):
    container2.empty()
    with container:
        st.image(loading_image, use_column_width ="always")

    preds_df = taxipoint.get_sql_table("preds", sql_engine)
    preds = preds_df["y"].values
    rides_df = taxipoint.get_ride_data(sql_engine = sql_engine)
    t = taxipoint.time_now_15()

    fig = taxipoint.print_forecast(preds, rides_df, t, sql_engine=sql_engine)

    container.empty()

    im = pio.write_image(fig, "plot.png", width=6*200, height=2.5*200, scale=3)

with container2:
    st.image("plot.png", use_column_width ="always")

