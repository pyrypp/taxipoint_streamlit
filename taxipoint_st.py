try:
    import streamlit as st
    import taxiplot
    from sqlalchemy import create_engine
    import os
    import time
    import requests


    import plotly.io as pio
    from PIL import Image
    from io import BytesIO


    # # #
    os.environ['TZ'] = 'Europe/Helsinki'
    time.tzset()

    db_str = st.secrets["db_str"]
    sql_engine = create_engine(db_str)


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

    with st.spinner("Loading..."):
        response = requests.get("https://taxipoint-pp.s3.eu-north-1.amazonaws.com/plot_sum.png", stream=True)
        im = Image.open(BytesIO(response.content))
        st.image(im, use_column_width ="always")

    st.write("VAIN MENEVÄ:")
    with st.spinner("Loading..."):
        response = requests.get("https://taxipoint-pp.s3.eu-north-1.amazonaws.com/plot_sum_me.png", stream=True)
        im = Image.open(BytesIO(response.content))
        st.image(im, use_column_width ="always")

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

            if submitted:
                with st.spinner("Odota..."):
                    taxiplot.save_to_sql_feedback(arvosana, teksti, sql_engine)
                    st.write("Palaute lähetetty. Kiitos!")
    
    st.write("---")


    st.markdown("""
        **v1.1.0** (16.8.2024)  

        Päivitys:
        Sivusto latautuu huomattavasti nopeammin. Latausaikaa nopeutettu yli 10 sekunnista alle sekuntiin.
    """)

    st.write("")

    st.markdown("""
        **v1.0.0** - (12.8.2024)  

        Sovelluksen ensimmäinen julkinen versio. Kuvaaja näyttää kysynnän edelliseltä 24 tunnilta ja ennusteen seuraavalle 24 tunnille. Ruuhkahuiput on väritetty. Ruuhkahuippujen yhteydessä on luku, joka kertoo, montako asiakasta ruuhkahuipussa on.

        Sovelluksesta löytyy myös palautelaatikko.
    """)

except:
    st.error("Palvelu on tällä hetkellä pois käytöstä! Pahoittelut.")

