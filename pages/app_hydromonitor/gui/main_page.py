# Generic packages
import streamlit as st
import logging
import os
from PIL import Image

# Obtain a logger for this module
logger = logging.getLogger(__name__)

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
    st.image(
        Image.open(
            os.path.join(os.path.dirname(__file__), '..', 'assets', 'WRIJ_Sweco.jpg')
        )
    )
    # Title
    st.title('BRO data naar Hydromonitor - tool')

    ## Output and editing table:
    # ===================================
    with st.container():
        if not st.session_state['output']['import_df'].empty:
            # Create CSV
            csv = st.session_state['output']['import_df'].to_csv(index=False, header=False).encode('utf-8')
            # Add blank lines to CSV
            '''The CSV is of type "bytes", like strings it is possible to replace sections.
            Here I replaced the empty line (shown as ",,,,,,,,,,,,") with "'\r\n\n'" to
            create a true blank line and not a line with empty cells''' 
            csv = csv.replace(b'\r\n,,,,,,,,,,,,\r\n', bytes('\r\n\n', encoding='utf8'))
            
            # Create download button 
            st.download_button(
                label="Download data als CSV",
                data=csv,
                file_name="testfile.csv",
                mime="text/csv",
            )
        st.dataframe(st.session_state['output']['import_df'], use_container_width=True)
        # Prevent 'hoover' download in gui, force user to use download button above
        st.markdown(
                """
                <style>
                [data-testid="stElementToolbar"] {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True
            )