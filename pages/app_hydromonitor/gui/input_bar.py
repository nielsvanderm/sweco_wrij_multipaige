import streamlit as st
import logging
from datetime import datetime
import pandas as pd

# Obtain a logger for this module
logger = logging.getLogger(__name__)

def create_parameters_list():
    return [
        {
            'parameter': 'import_df', 
            'label': 'Bestand', 
            'value_type':'file'},        
        {
            'parameter': 'titel', 
            'label': 'Titel', 
            'value_type':'string',
            'default': ''},
        {
            'parameter': 'gebruikersnaam', 
            'label': 'Gebruikersnaam',
            'value_type':'string',
            'default': ''},
        {
            'parameter': 'periode_aangevraagd_start',
            'label': 'Periode aangevraagd start',
            'value_type':'date',
            'default': '01-01-1800'},
        {
            'parameter': 'periode_aangevraagd_end', 
            'label': 'Periode aangevraagd eind',
            'value_type':'date',
            'default': datetime.now().strftime('%d-%m-%Y')},
        {
            'parameter': 'gegevens_beschikbaar_start', 
            'label': 'Gegevens beschikbaar start',
            'value_type':'date',
            'default': '01-01-1800'},
        {
            'parameter': 'gegevens_beschikbaar_end', 
            'label': 'Gegevens beschikbaar eind',
            'value_type':'date',
            'default': '01-01-1800'},
        {
            'parameter': 'datum', 
            'label': 'Datum',
            'value_type':'date',
            'default': datetime.now().strftime('%d-%m-%Y')},
        {
            'parameter': 'locatie', 
            'label': 'Locatie',
            'value_type':'string',
            'default': ''},
        {
            'parameter': 'filternummer', 
            'label': 'Filternummer',
            'value_type':'number',
            'number_format': '%d',
            'number_value_min': 1,
            'number_value_max': 99999,
            'number_step': 1,
            'default': 1},
        {
            'parameter': 'externe_aanduiding', 
            'label': 'Externe aanduiding',
            'value_type':'string', 
            'default': ''},
        {
            'parameter': 'xcordinaat', 
            'label': 'X-coördinaat',
            'value_type':'number',
            'number_format': '%d',
            'number_value_min': 0,
            'number_value_max': 99999,
            'number_step': 1,            
            'default': 0},
        {
            'parameter': 'ycordinaat', 
            'label': 'Y-coördinaat',
            'value_type':'number',
            'number_format': '%d',
            'number_value_min': 0,
            'number_value_max': 99999,
            'number_step': 1,            
            'default': 0},
        {
            'parameter': 'mv_tov_nap', 
            'label': 'MV t.o.v. NAP',
            'value_type':'number',
            'number_format': '%.2f',
            'number_value_min': -9999.00,
            'number_value_max': 99999.00,
            'number_step': 0.10,             
            'default': 0.00},
        {
            'parameter': 'datum_mv', 
            'label': 'Datum MV',
            'value_type':'date', 
            'default': '01-01-1800'},
        {
            'parameter': 'datum_start', 
            'label': 'Datum Start',
            'value_type':'date', 
            'default': '01-01-1800'},
        {
            'parameter': 'datum_end', 
            'label': 'Datum Eind',
            'value_type':'date', 
            'default': '01-01-1800'},
        {
            'parameter': 'mp_tov_nap', 
            'label': 'MP t.o.v. NAP',
            'value_type':'number',
            'number_format': '%.2f',
            'number_value_min': -9999.00,
            'number_value_max': 99999.00,
            'number_step': 0.10,            
            'default': 0.00},
        {
            'parameter': 'mp_tov_mv', 
            'label': 'MP t.o.v. MV',
            'value_type':'number',
            'number_format': '%.2f',
            'number_value_min': -9999.00,
            'number_value_max': 99999.00,
            'number_step': 0.10,            
            'default': 0.00},
        {
            'parameter': 'filter_boven', 
            'label': 'Filter Boven',
            'value_type':'number',
            'number_format': '%.2f',
            'number_value_min': -9999.00,
            'number_value_max': 99999.00,
            'number_step': 0.10,            
            'default': 0.00},
        {
            'parameter': 'filter_onder', 
            'label': 'Filter Onder',
            'value_type':'number',
            'number_format': '%.2f',
            'number_value_min': -9999.00,
            'number_value_max': 99999.00,
            'number_step': 0.10,            
            'default': 0.00}, 
    ]

def create_input_bar():
    params = {}
    for parameter in create_parameters_list():
        if parameter['value_type'] == 'number':
            params[parameter['parameter']] = st.number_input(
                label=parameter['label'],
                format=parameter['number_format'],
                step=parameter['number_step'],
                value=parameter['default'],
                min_value=parameter['number_value_min'],
            )
        elif parameter['value_type'] == 'date':
            params[parameter['parameter']] = st.date_input(
                label=parameter['label'],
                value=datetime.strptime(parameter['default'], '%d-%m-%Y').date()
            )
        elif parameter['value_type'] == 'string':
            params[parameter['parameter']] = st.text_input(
                label=parameter['label'],
                value=parameter['default']
            )
        elif parameter['value_type'] == 'file':
            input_file = st.file_uploader(
                label=parameter['label'],
                accept_multiple_files=False,
                type=['xlsx', 'xls'],
            )
            params[parameter['parameter']] = pd.DataFrame(input_file)
            if params[parameter['parameter']].empty:
                params[parameter['parameter']] = pd.DataFrame(input_file)
            else:
                df = pd.read_excel(input_file, sheet_name=0)
                params[parameter['parameter']] = df
    return params

def input_bar():
    with st.sidebar:
        st.session_state['output'] = create_input_bar()
