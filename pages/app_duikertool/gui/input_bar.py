import streamlit as st
import logging
import os
from PIL import Image

# Obtain a logger for this module
logger = logging.getLogger(__name__)
# Obtain dir for this module
dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'input_bar')


def input_bar():
    logger.debug(f"Sidebar input activated")

    ## Widgets for main input
    # ======================================
    with st.sidebar:
        culvert_diameter = st.number_input(
            label='Diameter [m]',
            format="%.2f",
            step=0.10,
            value=0.50,
            min_value=0.10,
        )
        culvert_length = st.number_input(
            label='Lengte [m]',
            format="%.2f",
            step=1.00,
            value=15.00,
            min_value=0.10,
            max_value=999.00,
        )
        # Here using *100 and *0.001 for the user to see in cm not in m, output is the same
        culvert_slope = st.number_input(
            label='verval duiker [cm]',
            format="%.2f",
            step=1.0,
            value=(culvert_diameter * 0.1) * 100,
            min_value=0.00,
            max_value=999.00,
        )*0.01
        soil_column_culvert = st.number_input(
            label='Gedeelde duiker ondergronds (door slib of begraving) [m]',
            format="%.2f",
            step=0.01,
            value=0.05,
            min_value=0.00,
            max_value=culvert_diameter,
        )
        culvert_crown = st.number_input(
            label='Bovenkant onderkant koker (bok) [m+NAP]',
            format="%.2f",
            step=1.00,
            value=0.00,
            min_value=0.00,
            max_value=999.00,
        )
        cover_depth = st.number_input(
            label='Grondlaag op duiker [cm]',
            format="%.2f",
            step=0.10,
            value=culvert_diameter * 0.3, 
            min_value=0.00,
            max_value=999.00,
        )

        ## Widgets for friction
        # ======================================
        with st.expander('Weerstandsopties'):

            ## Algemene verglijking:
            # --------------------------------------
            st.write('Algemene verglijking voor weerstandsverliezen')
            st.image(
                image=Image.open(f"{dir}/algemeen/weerstandsverglijking.png"),
                # caption='Algemene verglijking voor weerstandsverliezen'
            )            

            ## Intree weerstand:
            # --------------------------------------
            st.write('Intreeweerstand (§u)')
            st.image(
                image=Image.open(f"{dir}/intree/intree.jpg"),
                caption='Vormen van instroomopeningen met bijbehorende §-waarden. Standaardwaarde is 0,4'
            )
            inlet_flow_resistance = st.number_input(
                label='Selectie (§u)',
                format="%.2f",
                step=1.00,
                value=0.4,
                min_value=0.0,
                max_value=1.5,
            )

            ## Manning (wrijving verlies):
            # --------------------------------------
            st.write('Wrijvingsverlies (§w)')
            st.image(
                image=Image.open(f"{dir}/manning/wrijvingsverglijking.png"),
                # caption='Algemene verglijking voor wrijvingsverliezen'
            )
            st.image(
                image=Image.open(f"{dir}/manning/manning_values.jpg"),
                caption='Km-waarden voor betonnen duikers (Ven te Chow, 1959). Standaard waarde is 75.'
            )
            manning_roughness_coefficient = st.number_input(
                label='Selectie Km-waarde (manning)',
                format="%.2f",
                step=1.00,
                value=75.00,
                min_value=50.00,
                max_value=100.00,
            )

            ## Uittreeverliezen:
            # --------------------------------------
            st.write('Uittreeverlies (§u)')
            st.image(
                image=Image.open(f"{dir}/uittree/uittreeverliesverglijking.jpg"),
                caption='Bij k = 1 gaat de totale resterende kinetische energie verloren en bij k = 0 niet. Indien geen speciale voorzieningen voor het stroomlijnen van de uitstroomopening wordt genomen, wordt bij de berekening van waterlopenplannen meestal k = 1 aangenomen.'
            )
            n_parallel_culverts = st.number_input(
                label='Aantal naast elkaar gelegen duikers (a)',
                step=1,
                value=1,
                min_value=1,
                max_value=5,
            )
            wetted_area_channel_downstream = st.number_input(
                label='Natte oppervlak benedenstroomse waterloop (α)',
                format="%.2f",
                step=1.00,
                value=5.00,
                min_value=1.00,
                max_value=100.00,
            )
            outlet_shape_coefficient = st.number_input(
                label='Coëfficiënt afhankelijk van de vorm van de uitstroomopening van de duiker (k)',
                format="%.2f",
                step=0.10,
                value=1.00,
                min_value=0.00,
                max_value=1.00,
            )

            ## Bocht en knick verliezen:
            # --------------------------------------
            st.write('Bocht- en knikverliezen (§b en §k)')
            st.image(
                image=Image.open(f"{dir}/bocht_knik/tabel_bocht_knik.jpg"),
                caption='Bocht- en knikverliezen (Huisman, 1969). Bij rechte duikers is §b en §k 0'
            )
            bend_loss_coefficient = st.number_input(
                label='Bochtverliezen (§b)',
                format="%.2f",
                step=0.10,
                value=0.00,
                min_value=0.00,
                max_value=1.00,
            )
            n_bends = st.number_input(
                label='Aantal bochten',
                step=1,
                value=0,
                min_value=0,
                max_value=10,
            )
            # weerstand_knik = st.number_input(
            #     label='Knikverliezen (§k)',
            #     format="%.2f",
            #     step=0.10,
            #     value=0.00,
            #     min_value=0.00,
            #     max_value=2.00,
            # )
            # weerstand_bocht_aantal_knik = st.number_input(
            #     label='aantal knikken',
            #     step=1,
            #     value=0,
            #     min_value=0,
            #     max_value=10,
            # )
        

        option_discharge_backwater = st.radio(
            label='Bereken het debiet of de opstuwing',
            options=['Debiet', 'Opstuwing'],
            captions=['Bereken debiet obv opstuwing', 'Bereken opstuwing obv debiet'],
            horizontal=False,
        )
        
        ## Calculate discharge:
        # --------------------------------------
        if option_discharge_backwater == 'Debiet':
            discharge = None
            option_backwater = st.radio(
                label='Bereken verval water obv. verval of waterhoogtes',
                options=['verval', 'waterhoogtes'],
                horizontal=False,
            )
            water_column_upstream = st.number_input(
                label='Hoogte waterkolom bovenstrooms [m]',
                format="%.2f",
                step=0.10,
                value=culvert_diameter, 
                min_value=0.00,
                max_value=999.00,
            )            
            if option_backwater == 'verval':
                # Here using *0.01 for the user to see in cm not in m, output is the same
                backwater = st.number_input(
                    label='Opstuwing water [cm]',
                    format="%.2f",
                    step=0.10,
                    # Not 100% sure it works correct now
                    value=5.0 if culvert_slope < 5.0 else culvert_slope,
                    min_value=0.00,
                    max_value=999.00,
                ) * 0.01
                water_column_downstream = water_column_upstream - backwater
            else:
                water_column_downstream = st.number_input(
                    label='Hoogte waterkolom benedenstrooms [m]',
                    format="%.2f",
                    step=0.10,
                    value=water_column_upstream,
                    min_value=0.00,
                    max_value=999.00,
                )
                backwater = water_column_upstream - water_column_downstream
        
        ## Calculate backwater:
        # --------------------------------------
        else:
            backwater = None
            water_column_upstream = culvert_diameter
            water_column_downstream = st.number_input(
                label='Hoogte waterkolom benedenstrooms [m]',
                format="%.2f",
                step=0.10,
                value=water_column_upstream,
                min_value=0.00,
                max_value=999.00,
            )
            discharge = st.number_input(
                label='Debiet [m³ s⁻¹]',
                format="%.2f",
                step=0.10,
                value=0.10,
                min_value=0.00,
                max_value=999.00,
            )

        ## Return alle waardes:
        # --------------------------------------
        left_bar_input = dict(
            culvert_diameter=culvert_diameter,
            culvert_length=culvert_length,
            culvert_slope=culvert_slope,
            soil_column_culvert=soil_column_culvert,
            culvert_crown=culvert_crown,
            water_column_upstream=water_column_upstream,
            cover_depth=cover_depth,
            inlet_flow_resistance=inlet_flow_resistance,
            manning_roughness_coefficient=manning_roughness_coefficient,
            n_parallel_culverts=n_parallel_culverts,
            wetted_area_channel_downstream=wetted_area_channel_downstream,
            outlet_shape_coefficient=outlet_shape_coefficient,
            bend_loss_coefficient=bend_loss_coefficient,
            n_bends=n_bends,
            water_column_downstream=water_column_downstream,
            discharge=discharge,
            backwater=backwater,
            option_discharge_backwater=option_discharge_backwater,
            # option_backwater=option_backwater,
            # weerstand_knik=weerstand_knik,
            # weerstand_bocht_aantal_knik=weerstand_bocht_aantal_knik
        )

        st.session_state['input'] = left_bar_input

        return left_bar_input