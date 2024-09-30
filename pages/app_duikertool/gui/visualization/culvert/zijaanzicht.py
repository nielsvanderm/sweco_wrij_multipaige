##############################################################################
## Created on Fri Aug 25 14:04:11 2023                                      ##
## Author: Niels van der Maaden                                            	##
##                                                                        	##
##                         -- Zijaanzicht --                            	##
##                                                                          ##
## Dit bestand plot het zijaanzicht van de duiker                           ##
##############################################################################

'''
To do:
    1. tekst + pijlen cover_depth
    2. Toevoegen hoogtes (waterkolom beneden+boven, hoogte cover_depth, hoogte bok benedenstrooms+bovenstrooms)
    3. overstroming aangeven
'''


## Import packages:
# ============================================================================
import plotly.graph_objects as go
from pydantic import BaseModel
from . import GraphOptions as gop
from . import GraphUtils as gu
from .arceringen import Arceringen as ac

import streamlit as st

class Zijaanzicht(BaseModel):

    ## Duiker parameters
    # -------------------------------
    culvert_diameter: float = None
    culvert_length: float = None
    culvert_slope: float = None
    culvert_crown: float = 0

    ## Randvoorwaarden
    #-------------------------------
    soil_column_culvert: float = None
    discharge: float = None
    water_column_upstream: float = None
    water_column_downstream: float = None

    ## Weerstand
    #-------------------------------
    inlet_flow_resistance: float = None
    # mu_w: float = None
    # mu_u: float = None

    ## Opmaak
    #-------------------------------
    cover_depth: float = 0.4            ####
    embankment_slope_left : float = None
    embankment_slope_right : float = None

    ## aan/uit opties
    #-------------------------------
    knop_discharge: bool = True
    knop_verval_duiker: bool = True
    knop_verval_waterkolom: bool = True
    knop_weerstand: bool = True
    knop_lengte: bool = True
    knop_soil_column_culvertlaag: bool = True
    
    
    ## Initialize:
    # =======================================
    def __init__(self, **data):
        super().__init__(**data)


        ## Forceer waarde cover_depth:
        # --------------------------------------
        if not self.cover_depth:
            self.cover_depth = self.culvert_diameter * 2

        ## Fictief talud:
        # --------------------------------------
        self.embankment_slope_right  = (self.culvert_length * 0.3) / self.cover_depth
        self.embankment_slope_left  = (self.culvert_length * 0.2) / self.cover_depth
        if (self.cover_depth + self.culvert_slope) * self.embankment_slope_right  >= self.culvert_length * 0.6:
            self.embankment_slope_right  = self.embankment_slope_right  * 0.2

        ## Forceer waarde soil_column_culvert:
        # --------------------------------------
        if not self.soil_column_culvert:
            self.soil_column_culvert = 0

    ## Duiker:
    # ======================================
    def plot_duiker(self, fig):
        d, L, bok, verval = self.culvert_diameter, self.culvert_length, self.culvert_crown, self.culvert_slope
        
        ## Duiker xy:
        # --------------------------------------
        xy_duiker_linksonder = [
            0,
            bok
        ]
        xy_duiker_rechtsonder = [
            xy_duiker_linksonder[0] + L,
            xy_duiker_linksonder[1] - verval
        ]
        xy_duiker_rechtsboven = [
            xy_duiker_rechtsonder[0],
            xy_duiker_rechtsonder[1] + d
        ]
        xy_duiker_linksboven = [
            xy_duiker_linksonder[0],
            xy_duiker_linksonder[1] + d
        ]
        
        ## Plot onderkant duiker:
        # --------------------------------------
        fig.add_trace(
            go.Scatter(
                x=[
                    xy_duiker_linksonder[0],
                    xy_duiker_rechtsonder[0],
                ],
                y=[
                    xy_duiker_linksonder[1],
                    xy_duiker_rechtsonder[1],
                ],
                line=dict(width=15, color='black'),
                mode='lines',
                showlegend=False,
            )
        )
        
        ## Plot bovenkant duiker:
        # --------------------------------------
        fig.add_trace(
            go.Scatter(
                x=[
                    xy_duiker_rechtsboven[0],
                    xy_duiker_linksboven[0],
                ],
                y=[
                    xy_duiker_rechtsboven[1],
                    xy_duiker_linksboven[1],
                ],
                line=dict(width=15, color='black'),
                mode='lines',
                showlegend=False,
            )
        )
        return fig

    ## Watergang:
    # ======================================
    def plot_watergang(self, fig):
        d, L, bok, verval, cover_depth = self.culvert_diameter, self.culvert_length, self.culvert_crown, self.culvert_slope, self.cover_depth

        ## Watergang xy:
        # --------------------------------------
        xy_watergang_links = [
        	L * -0.5,
            bok
        ]
        xy_duiker_links = [
            0,
            bok
        ]
        xy_duiker_rechts = [
            xy_duiker_links[0] + L,
            xy_duiker_links[1] - verval
        ]
        xy_watergang_rechts = [
        	xy_duiker_rechts[0] + L * 0.5,
            xy_duiker_rechts[1]
        ]
        
        ## Plot watergang:
        # --------------------------------------
        fig.add_trace(
            go.Scatter(
                x=[
                    xy_watergang_links[0],
                    xy_duiker_links[0],
                    xy_duiker_rechts[0],
                    xy_watergang_rechts[0],
                ],
                y=[
                    xy_watergang_links[1],
                    xy_duiker_links[1],
                    xy_duiker_rechts[1],
                    xy_watergang_rechts[1],
                ],
                line=dict(width=2, color='black'),
                mode='lines',
                showlegend=False,
            )
        )
        
        # Plot maaiveld arcering:
        # --------------------------------------        
        fig = ac.plot_arcering_maaiveld(
            fig=fig,
            x_centre=(xy_duiker_links[0] + xy_watergang_links[0])/2,
            y_top=xy_watergang_links[1],
            size_x= L * 0.01,
            size_y = (verval + d + cover_depth) * 0.02,
        )
        fig = ac.plot_arcering_maaiveld(
            fig=fig,
            x_centre=(xy_duiker_rechts[0] + xy_watergang_rechts[0])/2,
            y_top=xy_watergang_rechts[1],
            size_x=L * 0.01,
            size_y=(verval + d + cover_depth) * 0.02,
        )
        
        return fig
        
    ## cover_depth:
    # ======================================
    def plot_cover_depth(self, fig):
        cover_depth, d, L, bok, verval, embankment_slope_left , embankment_slope_right  = self.cover_depth, self.culvert_diameter, self.culvert_length, self.culvert_crown, self.culvert_slope, self.embankment_slope_left , self.embankment_slope_right 

        ## cover_depth xy:
        # --------------------------------------
        xy_cover_depth_linksonder = [
            0,
            bok + d
        ]
        xy_cover_depth_rechtsonder = [
            L,
            bok + d - verval
        ]
        xy_cover_depth_rechtsboven = [
            L - ((cover_depth + verval) * embankment_slope_right ),
            bok + d + cover_depth
        ]
        xy_cover_depth_linksboven = [
        	cover_depth * embankment_slope_left ,
            bok + d + cover_depth
        ]

        ## Plot cover_depth:
        # --------------------------------------
        fig.add_trace(
            go.Scatter(
                x=[
                    xy_cover_depth_linksonder[0],
                    xy_cover_depth_rechtsonder[0],
                    xy_cover_depth_rechtsboven[0],
                    xy_cover_depth_linksboven[0],
                    xy_cover_depth_linksonder[0],
                ],
                y=[
                    xy_cover_depth_linksonder[1],
                    xy_cover_depth_rechtsonder[1],
                    xy_cover_depth_rechtsboven[1],
                    xy_cover_depth_linksboven[1],
                    xy_cover_depth_linksonder[1],
                ],
                line=dict(width=2, color='black'),
                mode='lines',
                showlegend=False,
                # Vul de plot 
                fill='toself',
                fillcolor='rgba(164, 164, 166, 255)'
            )
        )
        
        return fig
        
    ## Plot waterlijn:
    # ======================================
    def plot_waterlijn(self, fig):
        water_column_upstream, water_column_downstream, L, bok, d, verval, cover_depth, embankment_slope_left , embankment_slope_right  = self.water_column_upstream, self.water_column_downstream, self.culvert_length, self.culvert_crown, self.culvert_diameter, self.culvert_slope, self.cover_depth, self.embankment_slope_left , self.embankment_slope_right 
                        
        ## Waterlijn xy:
        # --------------------------------------
        xy_waterlijn_links_linksboven = [
            -L/2,
            water_column_upstream + bok
        ]
        xy_waterlijn_links_rechtsboven = [
            (water_column_upstream - d) * embankment_slope_left  if d < water_column_upstream else 0,
            water_column_upstream + bok
        ]
        xy_waterlijn_links_bovenkant_duiker = [
            0, 
            d + bok if d < water_column_upstream else water_column_upstream + bok
        ]
        xy_waterlijn_rechts_bovenkant_duiker = [
            L,
            bok + d - verval if d <= water_column_downstream else bok + water_column_downstream - verval
        ]
        xy_waterlijn_rechts_linksboven = [
            L - ((water_column_downstream - d) * embankment_slope_right ), #if d <= water_column_downstream else L,
            water_column_downstream + bok - verval
        ]
        xy_waterlijn_rechts_rechtsboven = [
            L + L/2, 
            water_column_downstream + bok - verval
        ]
        xy_waterlijn_rechts_rechtsonder = [
            L + L/2, 
            bok - verval
        ]
        xy_waterlijn_rechts_onderkant_duiker = [
            L, 
            bok - verval
        ]          
        xy_waterlijn_links_onderkant_duiker = [
            0,
            bok
        ]
        xy_waterlijn_links_linksonder = [
            -L/2,
            bok
        ]
        
        ## Plot waterlijn links, rechts:
        # --------------------------------------
        fig.add_trace(
            go.Scatter(
                x=[
                    xy_waterlijn_links_linksboven[0],
                    xy_waterlijn_links_rechtsboven[0],
                    xy_waterlijn_links_bovenkant_duiker[0],
                    xy_waterlijn_rechts_bovenkant_duiker[0],
                    xy_waterlijn_rechts_linksboven[0],
                    xy_waterlijn_rechts_rechtsboven[0],
                    xy_waterlijn_rechts_rechtsonder[0],
                    xy_waterlijn_rechts_onderkant_duiker[0],
                    xy_waterlijn_links_onderkant_duiker[0],
                    xy_waterlijn_links_linksonder[0],
                ],
                y=[
                    xy_waterlijn_links_linksboven[1],
                    xy_waterlijn_links_rechtsboven[1],
                    xy_waterlijn_links_bovenkant_duiker[1],
                    xy_waterlijn_rechts_bovenkant_duiker[1],
                    xy_waterlijn_rechts_linksboven[1],
                    xy_waterlijn_rechts_rechtsboven[1],
                    xy_waterlijn_rechts_rechtsonder[1],
                    xy_waterlijn_rechts_onderkant_duiker[1],
                    xy_waterlijn_links_onderkant_duiker[1],
                    xy_waterlijn_links_linksonder[1],
                ],
                line=dict(width=2, color='black'),
                mode='lines',
                showlegend=False,
                # Vul de plot 
                fill='toself',
                fillcolor='rgba(0, 102, 204, 0.5)'
            )
        )

        # Plot waterlijn arcering:
        # --------------------------------------
        fig = ac.plot_arcering_waterlijn(
            fig=fig,
            x_centre = L * -0.25,
            y_top = xy_waterlijn_links_rechtsboven[1],
            size_x=L * 0.15,
            size_y=(verval + d + cover_depth) * 0.6,
        )
        fig = ac.plot_arcering_waterlijn(
            fig=fig,
            x_centre = L * 1.25,
            y_top = xy_waterlijn_rechts_rechtsboven[1],
            size_x=L * 0.15,
            size_y=(verval + d + cover_depth) * 0.6,
        )

        return fig

    ## Plot soil_column_culvertlaag:
    # ======================================
    def plot_soil_column_culvertlaag(self, fig):
        L, bok, verval, soil_column_culvert = self.culvert_length, self.culvert_crown, self.culvert_slope, self.soil_column_culvert

        ## soil_column_culvert xy:
        # --------------------------------------
        xy_watergang_linksonder = [
            L * -0.5,
            bok
        ]
        xy_duiker_linksonder = [
            0,
            bok
        ]
        xy_duiker_rechtsonder = [
            L,
            bok - verval
        ]
        xy_watergang_rechts = [
            L * 1.25,
            bok - verval
        ]
        xy_duiker_rechtsboven = [
            L,
            bok - verval + soil_column_culvert
        ]
        xy_duiker_linksboven = [
            0,
            bok + soil_column_culvert
        ]
        xy_watergang_linksboven = [
            L * -0.5,
            bok + soil_column_culvert
        ]

        ## Plot soil_column_culvertlaag:
        # --------------------------------------
        fig.add_trace(
            go.Scatter(
                x=[
                    xy_watergang_linksonder[0],
                    xy_duiker_linksonder[0],
                    xy_duiker_rechtsonder[0],
                    xy_watergang_rechts[0],
                    xy_duiker_rechtsboven[0],
                    xy_duiker_linksboven[0],
                    xy_watergang_linksboven[0],
                ],
                y=[
                    xy_watergang_linksonder[1],
                    xy_duiker_linksonder[1],
                    xy_duiker_rechtsonder[1],
                    xy_watergang_rechts[1],
                    xy_duiker_rechtsboven[1],
                    xy_duiker_linksboven[1],
                    xy_watergang_linksboven[1],
                ],
                line=dict(width=2, color='black'),
                # line_shape='spline',
                mode='lines',
                showlegend=False,
                # Vul de plot
                fill='toself',
                fillcolor='rgba(112, 72, 60, 1)'
            )
        )

        return fig

    ## Plot indicatie pijlen:
    # ======================================
    def plot_indicatie_pijlen(self, fig):
        d, L, bok, verval, water_column_upstream, water_column_downstream, embankment_slope_right , soil_column_culvert, cover_depth = self.culvert_diameter, self.culvert_length, self.culvert_crown, self.culvert_slope, self.water_column_upstream, self.water_column_downstream, self.embankment_slope_right , self.soil_column_culvert, self.cover_depth

        ## Lengte duiker:
        # --------------------------------------
        if self.knop_lengte:
            fig = gu.plot_pijl(
                fig=fig,
                xy_beginpunt=[
                    0,
                    bok - verval - 0.3 * d
                ],
                xy_eindpunt=[
                    L,
                    bok - verval - 0.3 * d
                ],
                line_width=4,
                marker_size = 20,
                marker_symbol='arrow-bar-up',
                tekst= f"Lengte = {L} m",
                textposition='middle center',
                tekst_offset_y= (d + cover_depth) * -0.1
            )

        ## soil_column_culvertlaag:
        # --------------------------------------
        if self.knop_soil_column_culvertlaag:
            fig = gu.plot_lijn(
                fig=fig,
                xy_beginpunt=[
                    L,
                    bok - verval + soil_column_culvert
                ],
                xy_eindpunt=[
                     L * 1.25,
                    bok - verval + soil_column_culvert
                ],
                line_width=2,
                line_dash='dash',
                color='grey'
            )
            fig = gu.plot_pijl(
                fig=fig,
                xy_beginpunt=[
                    L * 1.25,
                    bok - verval + soil_column_culvert
                ],
                xy_eindpunt=[
                    L * 1.25,
                    bok - verval
                ],
                line_width=2,
                marker_size = 10,
                tekst= f"Verzanding = {int(soil_column_culvert * 100)} cm",
                textposition='top left',
                tekst_offset_x= L * 0.2,
                tekst_offset_y= d - d + soil_column_culvert,
            )

        ## Verval duiker:
        # --------------------------------------
        if self.knop_verval_duiker:
            fig = gu.plot_lijn(
                fig=fig,
                xy_beginpunt=[
                    0,
                    bok - verval
                ],
                xy_eindpunt=[
                    L,
                    bok - verval
                ],
                line_width=2,
                line_dash='dash',
                color='grey'
            )
            fig = gu.plot_pijl(
                fig=fig,
                xy_beginpunt=[
                    0,
                    bok
                ],
                xy_eindpunt=[
                    0,
                    bok - verval
                ],
                line_width=2,
                marker_size = 10,
                tekst= f"Verval duiker = {int(verval*100)} cm",
                textposition='middle left',
                tekst_offset_x= 0.2* L if verval < 0.15 else -0.04* L,
                tekst_offset_y= bok - (verval * 1.1) if verval < 0.15 else (d + cover_depth) * -0.1
            )

        ## ∆h verval waterkolom:
        # --------------------------------------        
        if self.knop_verval_waterkolom:
            fig = gu.plot_lijn(
                fig=fig,
                xy_beginpunt=[
                    L - ((water_column_upstream - d + verval) * embankment_slope_right ) if d < water_column_upstream else 0,
                    water_column_upstream + bok
                ],
                xy_eindpunt=[
                    L + L/8,
                    water_column_upstream + bok
                ],
                line_width=1,
                line_dash='dash',
                color='grey'
            )
            fig = gu.plot_pijl(
                fig=fig,
                xy_beginpunt=[
                    L + L/8,
                    water_column_upstream + bok
                ],
                xy_eindpunt=[
                    L + L/8,
                    water_column_downstream + bok - verval
                ],
                line_width=1,
                marker_size = 10,
                tekst= f"Verval (∆h) = {round(water_column_upstream - water_column_downstream, 2)} m",
                textposition='middle right',
                tekst_offset_x= 0.01 * L,

            )
        
        ## discharge Q:
        # --------------------------------------    
        if self.knop_discharge:
            fig = gu.plot_pijl(
                fig=fig,
                xy_beginpunt=[
                    L * -0.3,
                    bok + water_column_upstream * 0.5
                ],
                xy_eindpunt=[
                    L * -0.4,
                    bok + water_column_upstream * 0.5
                ],
                dubble_pijl=False,
                line_width=2,
                marker_size = 15,
                tekst= f"Debiet (Q) = {round(self.discharge, 2)} m³ s⁻¹",
                textposition='middle center',
                tekst_offset_y= (d + cover_depth) * -0.1,
                tekst_offset_x=1.5
            )

        ## Weerstand §:
        # --------------------------------------
        if self.knop_weerstand:
            fig = gu.plot_tekst(
                fig=fig,
                xy_tekst=[
                    0,
                    bok + d * 0.5
                ],
                tekst=f"§i = {self.inlet_flow_resistance}",
                textposition='middle center',
            )
            fig = gu.plot_tekst(
                fig=fig,
                xy_tekst=[
                    0.5 * L,
                    bok + d * 0.5 - 0.5 * verval
                ],
                tekst=f"§w = {0.7}",
                textposition='middle center',
            )
            fig = gu.plot_tekst(
                fig=fig,
                xy_tekst=[
                    L,
                    bok - verval + d * 0.5
                ],
                tekst=f"§u = {0.1}",
                textposition='middle center',
            )

        return fig

    ## Plot figuur:
    # ======================================
    def plot_figuur(self):

        ## Maak een figuur aan:
        # --------------------------------------
        fig = go.Figure()

        ## Plot waterlijn:
        # --------------------------------------
        fig = self.plot_waterlijn(fig)

        ## Plot soil_column_culvertlaag:
        # --------------------------------------
        fig = self.plot_soil_column_culvertlaag(fig)
        
        ## Plot watergang:
        # --------------------------------------
        fig = self.plot_watergang(fig)
        
        ## Plot cover_depth:
        # --------------------------------------
        fig = self.plot_cover_depth(fig)
        
        ## Plot duiker:
        # --------------------------------------
        fig = self.plot_duiker(fig)
        
        ## Plot indicatie pijlen:
        # --------------------------------------
        fig = self.plot_indicatie_pijlen(fig)
        
        ## Grafiek opties:
        # --------------------------------------
        fig = gop.duiker_grafiekopties_zijaanzicht(
            fig =fig,
            title = 'Duiker zijaanzicht'
        )
        
        ## Toon figuur:
        # --------------------------------------
        # fig.show()
        return fig