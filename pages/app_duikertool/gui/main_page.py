##############################################################################
## Created on Fri Aug 25 14:04:11 2023                                      ##
## Author: Niels van der Maaden                                             ##
##                                                                          ##
##                          --Hoofdpagina--                                 ##
##                                                                          ##
## Hier staat de hoofdpagina van de Streamlit app                           ##
##############################################################################
import streamlit as st
from PIL import Image
import os
import logging
from pages.app_duikertool.gui.visualization import visualization as vis
from pages.app_duikertool.culvert import culvert_calculator as cc

# Obtain a logger for this module
logger = logging.getLogger(__name__)

def markdown_regular(
    text_input:str = None):
    return st.markdown(f"<h1 style='text-align: left; color: black; font-size:20px;'>{text_input} </h1>", unsafe_allow_html=True)
def markdown_header(
    text_input:str = None):
    return st.markdown(f"<h1 style='text-align: left; color: black; font-size:30px;'>{text_input}</h1>", unsafe_allow_html=True)

def main_page():

    logger.debug(f"Main page activated")

    ## App info:
    # ===================================
    # Small text with name producer
    st.markdown(
        "<h1 style='text-align: right; color: black; font-size:10px;'>Geproduceerd door: Niels van der Maaden</h1>", 
        unsafe_allow_html=True
    )
    # Logo
    '''Use columns to outline the image to the right. 
    It's not perfect but fine for here.'''
    col1, col2, col3 = st.columns([1, 1, 2])
    with col3:
        st.image(
            Image.open(
                os.path.join(os.path.dirname(__file__), '..', 'assets', 'main_page', 'WRIJ_Sweco.jpg')
            ),
            width=500
        )
    
    # Title
    st.title('Duiker-tool')        

    ## Output and editing table:
    # ===================================
    with st.container():
        
        # Get user input
        input_bar = st.session_state['input']
        # print(f"input = {input_bar}")

        if input_bar['option_discharge_backwater'] == 'Debiet':
            result = cc.culvert_calculator(
                calculate = 'discharge',
                **input_bar)
        elif input_bar['option_discharge_backwater'] == 'Opstuwing':
            result = cc.culvert_calculator(
                calculate = 'backwater',
                **input_bar)
            result['water_column_upstream'] = result['water_column_downstream'] + result['backwater'] 
        print(f"RESULT = {result}")
        
        ## Output in figures:
        # ===================================
        plot = vis.PlotDuiker(
            cover_depth = input_bar['cover_depth'],
            **result)

        tab1, tab2 = st.tabs(['Zijaanzicht', 'Vooraanzicht'])
        with tab1:
            st.plotly_chart(plot.plot_zijaanzicht(), use_container_width=False)


        with tab2:
            st.plotly_chart(plot.plot_vooraanzicht(), use_container_width=False)
            # markdown_regular(f"Hier komt de vooraanzicht")

        ## Output in numbers:
        # ===================================        
        tab3, tab4 = st.tabs(['Resultaten', 'geavanceerde resultaten'])
        with tab3:
            markdown_regular(f"Debiet: {round(result['discharge'],3)} [m3/s]")
            markdown_regular(f"Stroomsnelheid: {round(result['flow_velocity'],3)} [m/s]")
            markdown_regular(f"Opstuwing: {round(result['backwater'],3)} [m]")

        with tab4:
            markdown_header('Generieke resultaten')
            markdown_regular(f"Debiet: {round(result['discharge'],3)} [m3/s]")
            markdown_regular(f"Stroomsnelheid: {round(result['flow_velocity'],3)} [m/s]")
            markdown_regular(f"Opstuwing: {round(result['backwater'],3)} [m]")

            markdown_header('Duiker eigenschappen')
            markdown_regular(f"Natte oppervlak: {round(result['wetted_area'],3)} [m2]")
            markdown_regular(f"Natte omtrek: {round(result['wetted_perimeter'],3)} [m]")
            markdown_regular(f"Hydrailische straal: {round(result['hydraulic_radius'],3)} [m]")

            markdown_header('Weerstand')
            markdown_regular(f"Weerstand totaal: {round(result['loss_coefficient'],3)} [????]")
            markdown_regular(f"Weerstand op basis van Manning: {round(result['roughness_coefficient'],3)} [????]")
            markdown_regular(f"Wrijvingsverlies: {round(result['friction_loss'],3)} [????]")
            markdown_regular(f"Uitreeverlies: {round(result['exit_loss'],3)} [????]")


        # Definieer de vereiste standaardwaarden voor de ontbrekende velden
        # default_values = {
        #     'gronddekking': 0.2,
        #     'h_uitstroom': 0.1,
        #     'duiker_verval': 0.5
        # }

        # Vul de session_state met de standaardwaarden als die ontbreken
        # for key, value in default_values.items():
        #     if key not in st.session_state['input']:
        #         st.session_state['input'][key] = value
        # print(f"culvert type = {type(culvert)}")
        # print(f"culvert type = {culvert}")
        # cc.CulvertCalculator(**st.session_state['input'])
        # Vervolgens roep je PlotDuiker aan
        # plot = vis.PlotDuiker(**st.session_state['input'])
        # st.plotly_chart(plot.plot_zijaanzicht(), use_container_width=False)
        # st.plotly_chart(plot.plot_vooraanzicht(), use_container_width=False)

        # st.plotly_chart(plot.plot_zijaanzicht())


    #..... Hier de rest van de app
