##############################################################################
## Created on Fri Aug 25 14:04:11 2023                                      ##
## Author: Niels van der Maaden                                             ##
##                                                                          ##
##                     -- __init.py bestand --                              ##
##                                                                          ##
## Dit is een __init__.py bestand                                           ##
##############################################################################

import app
import logging

def setup_logging():
    # Get root logger
    logger = logging.getLogger()

    # Delete existing handlers
    '''Streamlit's refreshing behavior creates duplicate handlers, 
    resulting in excessive logging messages.'''
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set logging configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='basic.log',
    )
    
    # Add handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(console_handler)

# Call app
    '''Invoke the app directly (not in if __name__ == "__main__") to ensure it runs 
    on every reload. Streamlit does not execute code in the main loop during refresh.'''
logger = logging.getLogger(__name__)
logger.info('Application booted')
app = app.AppDuikerTool()