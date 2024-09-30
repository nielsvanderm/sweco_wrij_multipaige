##############################################################################
## Created on Fri Aug 25 14:04:11 2023                                      ##
## Author: Niels van der Maaden                                             ##
##                                                                          ##
##                -- create maaiveld Arcering --                            ##
##                                                                          ##
## Dit bestand maakt de csv-bestand dat de maaiveld arcering representeerd  ##
##############################################################################

## Import packages:
# ============================================================================
from .culvert import vooraanzicht as vaz
from .culvert import zijaanzicht as zaz
from pydantic import BaseModel
import logging

# Verkrijg een logger voor deze module
logger = logging.getLogger(__name__)

class PlotDuiker(BaseModel):

    vooraanzicht: vaz.Vooraanzicht = None
    zijaanzicht: zaz.Zijaanzicht = None

    def __init__(self, **data):
        super().__init__(**data)
        self.vooraanzicht = vaz.Vooraanzicht(**data)
        self.zijaanzicht = zaz.Zijaanzicht(**data)

    def plot_vooraanzicht(self):
        vooraanzicht = self.vooraanzicht.plot_figuur()
        logger.debug('Vooraanzicht is geplot')
        return vooraanzicht

    def plot_zijaanzicht(self):
        zijaanzicht = self.zijaanzicht.plot_figuur()
        logger.debug('Zijaanzicht is geplot')
        return zijaanzicht


