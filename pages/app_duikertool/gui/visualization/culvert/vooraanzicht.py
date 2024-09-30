##############################################################################
## Created on Fri Aug 25 14:04:11 2023                               		##
## Author: Niels van der Maaden                             				##
##                        													##
##                              -- Vooraanzicht --          				##
##                                             								##
## Dit bestand plot het vooraanzicht van de duiker                          ##
##############################################################################

## Import packages:
# ============================================================================
import pandas as pd
import numpy as np
from pydantic import BaseModel
import plotly.graph_objects as go
from . import GraphOptions as gop
from . import GraphUtils as gu
from .arceringen import Arceringen as ac

class Vooraanzicht(BaseModel):

    ## Duiker parameters
    # -------------------------------
    culvert_diameter: float = None
    culvert_crown: float = 0

    ## Randvoorwaarden
    #-------------------------------
    soil_column_culvert: float = None
    air_column_culvert:float = None,
    water_column_upstream: float = None
    cover_depth:float = None

    ## Duiker:
    # ======================================
    def plot_duiker(self, fig):
        d, bok, soil_column_culvert, water_column_upstream = self.culvert_diameter, self.culvert_crown, self.soil_column_culvert, self.water_column_upstream
        r = d * 0.5

        ## Functie om (gedeeltelijke) cirkel te plotten:
        # --------------------------------------
        def plot_cirkel(
                fig, r:float = None, 
                y_min:float = None, 
                y_max:float = None, 
                color_fill:str = None, 
                color_line:str = None,
                fill:str = 'toself', 
                line_width:float =0.2
            ):

            ## Defineer boven- en ondergrens:
            # --------------------------------------
            y_min = -r + y_min
            y_max = -r + y_max

            # y-coordinaten van het deel van de cirkel dat je wilt plotten
            y = np.linspace(y_min, y_max, 100)

            # Bereken de bijbehorende x-coordinaten met de Pythagorese stelling
            x_positive = np.sqrt(r ** 2 - y ** 2)
            x_negative = -x_positive

            # Sluit de cirkel door de eerste en laatste punten te verbinden
            x = np.concatenate([x_negative, x_positive[::-1], x_negative[:1]])
            y = np.concatenate([y, y[::-1], y[:1]])

            x, y = x + r, y + r

            ## Plot (gedeeltelijke) cirkel:
            # --------------------------------------
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode='lines',
                    line=dict(width=line_width, color=color_line),
                    fill=fill,
                    fillcolor=color_fill,
                    hoverinfo='none',
                    showlegend=False,
                )
            )

            return fig

        ## Plot soil_column_culvert:
        # --------------------------------------
        plot_cirkel(
            fig=fig,
            r=r,
            y_min=0.0,
            y_max= min(soil_column_culvert, d),
            color_fill='rgba(112, 72, 60, 1)',
            color_line='grey'
        )

        ## Plot water:
        # --------------------------------------
        plot_cirkel(
            fig=fig,
            r=r,
            y_min=soil_column_culvert,
            y_max= min(water_column_upstream, d),
            color_fill='rgba(0, 102, 204, 0.5)',
            color_line='grey',
        )

        # ## Plot lucht:
        # # --------------------------------------
        plot_cirkel(
            fig=fig,
            r=r,
            y_min= min(water_column_upstream, d),
            y_max= d,
            color_fill='rgba(255, 255, 255, 1)',
            color_line='grey',
        )

        ## Plot duiker:
        # --------------------------------------
        plot_cirkel(
            fig=fig,
            r=r,
            y_min=0.0,
            y_max=d,
            color_line='black',
            fill='none',
            line_width=6
        )

        return fig

    ## Watergang:
    # ======================================
    def plot_watergang(self, fig, talud: float = 1.5, bodembreedte: float = None):
        d, soil_column_culvert, cover_depth = self.culvert_diameter, self.soil_column_culvert, self.cover_depth

        ## Forcings:
        # --------------------------------------
        if cover_depth is None:
            cover_depth = d * 0.2
        if bodembreedte is None:
            bodembreedte = d * 1.2

        r = d * 0.5
        maaiveld = d + cover_depth
        opmaak_grondbreedte = d

        ## Rechterkant watergang:
        # --------------------------------------
        xy_watergang_rechtsonder = [
            r + bodembreedte * 0.5,
            soil_column_culvert
        ]
        xy_watergang_rechtsboven = [
            xy_watergang_rechtsonder[0] + talud * (maaiveld + r - soil_column_culvert),
            maaiveld,
        ]
        xy_grond_rechtsboven = [
            xy_watergang_rechtsboven[0] + opmaak_grondbreedte,
            maaiveld
        ]

        ## Linkerkant watergang:
        # --------------------------------------
        xy_watergang_linksonder = [
            r - bodembreedte * 0.5,
            soil_column_culvert
        ]
        xy_watergang_linksboven = [
            -xy_watergang_rechtsboven[0],
            xy_watergang_rechtsboven[1]
        ]
        xy_grond_linksboven = [
            -xy_grond_rechtsboven[0],
            xy_grond_rechtsboven[1]
        ]

        ## Plot watergang:
        # --------------------------------------
        fig.add_trace(
            go.Scatter(
                x=[
                    xy_grond_linksboven[0],
                    xy_watergang_linksboven[0],
                    xy_watergang_linksonder[0],
                    xy_watergang_rechtsonder[0],
                    xy_watergang_rechtsboven[0],
                    xy_grond_rechtsboven[0],
                    xy_watergang_linksboven[0],
                ],
                y=[
                    xy_grond_linksboven[1],
                    xy_watergang_linksboven[1],
                    xy_watergang_linksonder[1],
                    xy_watergang_rechtsonder[1],
                    xy_watergang_rechtsboven[1],
                    xy_grond_rechtsboven[1],
                    xy_watergang_linksboven[1],
                ],
                line=dict(width=2, color='black'),
                mode='lines',
                showlegend=False,
            )
        )
        
        ## Maaiveld arcering:
        # --------------------------------------
        fig = ac.plot_arcering_maaiveld(
            fig=fig,
            x_centre=(xy_watergang_linksboven[0] + xy_grond_linksboven[0])/2,
            y_top=xy_grond_linksboven[1],
            size=d*0.03
        )
        fig = ac.plot_arcering_maaiveld(
            fig=fig,
            x_centre=(xy_watergang_rechtsboven[0] + xy_grond_rechtsboven[0])/2,
            y_top=xy_grond_rechtsboven[1],
            size=d*0.03
        )
        
        return fig

    ## Plot indicatie pijlen:
    # ======================================
    def plot_indicatie_pijlen(self, fig):
        soil_column_culvert, air_column_culvert, d, water_column_upstream = self.soil_column_culvert, self.air_column_culvert, self.culvert_diameter, self.water_column_upstream
        r = d * 0.5

        ## soil_column_culvert:
        # --------------------------------------
        fig = gu.plot_pijl(
            fig=fig,
            xy_beginpunt=[
                d * 1.04,
                0,
            ],
            xy_eindpunt=[
                d * 1.04,
                soil_column_culvert
            ],
            line_width=2,
            marker_size=10,
            marker_symbol='arrow-bar-up',
            tekst=f"Verzanding = {int(soil_column_culvert*100)} cm",
            textposition='middle right',
            tekst_offset_x= d * 0.05
        )

        ## Water:
        # --------------------------------------
        fig = gu.plot_pijl(
            fig=fig,
            xy_beginpunt=[
                d * 1.04,
                soil_column_culvert,
            ],
            xy_eindpunt=[
                d * 1.04,
                water_column_upstream
            ],
            line_width=2,
            marker_size=10,
            marker_symbol='arrow-bar-up',
            tekst=f"Waterhoogte = {int(water_column_upstream*100)} cm",
            textposition='middle right',
            tekst_offset_x= d * 0.05
        )

        ## Lucht:
        # --------------------------------------
        fig = gu.plot_pijl(
            fig=fig,
            xy_beginpunt=[
                d * 1.04,
                water_column_upstream,
            ],
            xy_eindpunt=[
                d * 1.04,
                d
            ],
            line_width=2,
            marker_size=10,
            marker_symbol='arrow-bar-up',
            tekst=f"Lucht = {int(air_column_culvert*100)} cm",
            textposition='middle right',
            tekst_offset_x= d * 0.05
        )

        ## plot diameter indicatie:
        # --------------------------------------
        x_end = (r * np.cos(np.radians(135))) + r
        y_end = (r  * np.sin(np.radians(135))) + r

        fig = gu.plot_pijl(
            fig=fig,
            xy_beginpunt=[
                x_end,
                y_end

            ],
            xy_eindpunt=[
                r,
                r,
            ],
            line_width=4,
            marker_size=20,
            color = 'red',
            marker_color_outline='red',
            dubble_pijl=False,
        )

        fig = gu.plot_tekst(
            fig=fig,
            xy_tekst=[
                x_end * 0.8,
                y_end
            ],
            tekst=f"Straal = {r} m",
            textposition='middle left'
        )

        return fig

    ## Plot vooraanzicht:
    # ======================================
    def plot_figuur(self, title: str = None):
        d, soil_column_culvert, water_column_upstream = self.culvert_diameter, self.soil_column_culvert, self.water_column_upstream
        r = d / 2
        offset = r * 1.2

        ## Maak een figuur aan:
        # --------------------------------------
        fig = go.Figure()

        ## Plot duiker
        # --------------------------------------
        fig = self.plot_duiker(fig=fig)

        ## Plot indicatie pijlen
        # --------------------------------------
        fig = self.plot_indicatie_pijlen(fig=fig)

        ## plot watergang:
        # --------------------------------------
        # fig = self.plot_watergang(fig=fig)

        ## Grafiek opties:
        # --------------------------------------
        fig = gop.duiker_grafiekopties_vooraanzicht(
            fig =fig,
            title = 'Duiker vooraanzicht, stroomopwaarde kant'
        )
        
        # Toon de figuur
        # fig.show()
        return fig