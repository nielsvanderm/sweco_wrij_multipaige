# Generic packages
import streamlit as st
from pydantic import BaseModel
import pandas as pd
import logging
# Local packages
from pages.app_hydromonitor.data import data_tools
from pages.app_hydromonitor.gui import input_bar
from pages.app_hydromonitor.gui import main_page

# Obtain a logger for this module
logger = logging.getLogger(__name__)

class AppHydromonitor(BaseModel):
    input_sidebar: dict = None

    def __init__(self, **data):
        super().__init__(**data)
        logger.info("AppHydromonitor initialized")
        self.run_app()

    def run_app(self):
        input_bar.input_bar()
        if not st.session_state['output']['import_df'].empty:
            st.session_state['output']['import_df'] = pd.DataFrame(
                data_tools.construct_exportfile(**st.session_state['output'])
            )
        main_page.main_page()
