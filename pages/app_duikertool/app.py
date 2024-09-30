##############################################################################
## Created on Fri Aug 25 14:04:11 2023                                      ##
## Author: Niels van der Maaden                                             ##
##                                                                          ##
##                              --App--                                     ##
##                                                                          ##
## Dit bestand voegt alle componenten van de app samen                      ##
##############################################################################

# Generic packages
from pydantic import BaseModel
import logging
import streamlit as st


# Local packages
from pages.app_duikertool.gui import main_page
from pages.app_duikertool.gui import input_bar
# from visualization import visualization as vis
# from culvert import culvert_calculator as cc
# from gui import Streamlit2


# Verkrijg een logger voor deze module
logger = logging.getLogger(__name__)

class AppDuikerTool(BaseModel):

    input_sidebar: dict = None

    def __init__(self, **data):
        super().__init__(**data)

        self.run_app()
        # self.input_sidebar = Streamlit2.invoer_sidebar()
        # self.duiker = dt.DuikerTool(**input_sidebar)

    def run_app(self):
        st.set_page_config(layout="wide")
        input_bar.input_bar()
        main_page.main_page()