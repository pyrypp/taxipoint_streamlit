try:
    import streamlit as st
    import taxipoint
    from sqlalchemy import create_engine
    import os
    import time

    import plotly.io as pio
    from PIL import Image

    # # #
    os.environ['TZ'] = 'Europe/Helsinki'
    time.tzset()

    db_str = st.secrets["db_str"]
    sql_engine = create_engine(db_str)

    # # #

    if 'first run' not in st.session_state:
        st.session_state['first run'] = True

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
        "<h2 style='text-align: center; color: black;'>Helsinki-Vantaan lentoasema  <br>Taksikysynnän ennuste</h2>", 
        unsafe_allow_html=True
    )


    # # #

    container_plot = st.empty()

    def get_loading_image():
        image = Image.open("plot.png")
        scale = 0.15
        w = int(3500 * scale)
        h = int(1500 * scale)
        image = image.resize((w,h))
        loading_image = image.convert("RGBA")
        data = image.getdata()
        new_data = []
        for item in data:
            new_data.append((item[0], item[1], item[2], 100))
        loading_image.putdata(new_data)
        return loading_image

    if st.session_state['first run']:
        loading_image = get_loading_image()


    if st.session_state['first run']:
        with st.spinner("Loading..."):
            container_loading_image = st.empty()
            container_plot.empty()
            with container_loading_image:
                st.image(loading_image, use_column_width ="always")

            t = taxipoint.time_now_15()
            preds_df = taxipoint.get_sql_table("preds", sql_engine)
            preds_df = preds_df[preds_df["datetime"]>=t]
            preds = preds_df["y"].values
            rides_df = taxipoint.get_ride_data(sql_engine = sql_engine)
            
            fig = taxipoint.print_forecast(preds, rides_df, t, sql_engine=sql_engine)

            im = pio.write_image(fig, "plot.png", width=6*200, height=2.5*200, scale=3)

            container_loading_image.empty()

    with container_plot:
        st.image("plot.png", use_column_width ="always")


    st.write("---")

    st.markdown("""
    Tämä palvelu tarjoaa ennusteen Helsinki-Vantaan lentokentän taksiaseman kysynnästä. Ennusteet perustuvat Taxipointin historiallista dataa hyödyntävään tekoälymalliin. Palvelu on tarkoitettu antamaan yleiskuvaa taksikysynnän vaihteluista eri ajankohtina.

    **Huomio:** Tämä projekti on harrasteprojekti, eikä virallinen palvelu. Ennusteet eivät ole taattuja. Suosittelen käyttämään ennustetta vain suuntaa-antavana tietona.


    \- Pyry Pohjanoksa
    """)

    st.write("---")

    col1, col2 = st.columns(2)
    with col1:  
        with st.form("feedback_form", clear_on_submit=True):
            st.write("Palautelaatikko")

            arvosana = st.feedback("stars")
            if arvosana != None:
                arvosana += 1

            teksti = st.text_input(label="label", placeholder="Vapaa sana...", max_chars=256, label_visibility="hidden")

            submitted = st.form_submit_button("Lähetä")

            st.session_state['first run'] = False
            if submitted:
                with st.spinner("Odota..."):
                    taxipoint.save_to_sql_feedback(arvosana, teksti, sql_engine)
                    st.write("Palaute lähetetty. Kiitos!")
except:
    st.error("Palvelu on tällä hetkellä pois käytöstä! Pahoittelut.")