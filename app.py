import streamlit as st
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class MultiPaige(BaseModel):

    def __init__(self, **data):
        super().__init__(**data)
        logger.info("MultiPaige initialized")
        self.run_app()

    def run_app(self):
        st.set_page_config(
            page_title='Multipage test'
        )
        st.title('main page')
        st.sidebar.success('selecteer pagina')
