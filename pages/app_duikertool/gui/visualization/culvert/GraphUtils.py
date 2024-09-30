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
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

## Plot tekst:
# ======================================
def plot_tekst(
    fig,
    xy_tekst=None,
    tekst: str = None,
    tekst_size: float = 14,
    tekst_color: float = 'black',
    tekst_family: str = 'Arial Black, Arial, sans-serif',
    textposition: str = 'middle center'):

    fig.add_trace(
        go.Scatter(
            x=[xy_tekst[0]],
            y=[xy_tekst[1]],
            text=[tekst],
            mode='text',
            textposition=textposition,
            textfont=dict(
                family=tekst_family,
                size=tekst_size,
                color=tekst_color,
            ),
            hoverinfo='none',
            showlegend=False
        )
    )

    return fig

## Plot indicatie lijnen:
# ======================================
def plot_lijn(
    fig,
    xy_beginpunt: list = None,
    xy_eindpunt: list = None,
    color: str = 'black',
    line_width: float = 4,
    line_dash: str = 'solid',

    tekst: str = None,
    tekst_size: float = 14,
    tekst_color: float = 'black',
    tekst_family:str = 'Arial Black, Arial, sans-serif',
    textposition: str = 'middle center',
    tekst_offset_x: float = None,
    tekst_offset_y: float = None):

    ## Voeg de lijn toe (zonder markers):
    # --------------------------------------
    fig.add_trace(
        go.Scatter(
            x=[xy_eindpunt[0], xy_beginpunt[0]],
            y=[xy_eindpunt[1], xy_beginpunt[1]],
            line=dict(width=line_width, color=color, dash=line_dash),
            mode='lines',
            hoverinfo='none',
            showlegend=False,
        )
    )

    if tekst:
        middelpunt_x = (xy_beginpunt[0] + xy_eindpunt[0]) * 0.5
        middelpunt_y = (xy_beginpunt[1] + xy_eindpunt[1]) * 0.5

        if tekst_offset_x:
            middelpunt_x += tekst_offset_x
        if tekst_offset_y:
            middelpunt_y += tekst_offset_y

        fig = plot_tekst(
            fig=fig,
            xy_tekst=[middelpunt_x, middelpunt_y],
            tekst=tekst,
            tekst_size=tekst_size,
            tekst_color=tekst_color,
            tekst_family=tekst_family,
            textposition=textposition

        )

        fig.add_trace(
            go.Scatter(
                x=[middelpunt_x],
                y=[middelpunt_y],
                text=[tekst],
                mode='text',
                textposition=textposition,
                textfont=dict(
                    family=tekst_family,
                    size=tekst_size,
                    color=tekst_color,
                ),
                hoverinfo='none',
                showlegend=False
            )
        )

    return fig

## Plot indicatie pijlen:
# ======================================
def plot_pijl(
    fig,
    xy_beginpunt: list = None,
    xy_eindpunt: list = None,
    line_width: float =4,
    line_dash: str ='solid',
    color: str = 'black',

    dubble_pijl: bool = True,
    marker_size: float = 20,
    marker_color: str = None,
    marker_color_outline: str =  'DarkSlateGrey',
    marker_symbol: str = 'arrow',

    tekst: str = None,
    tekst_size: float = 14,
    tekst_color: float = 'black',
    tekst_family:str = 'Arial Black, Arial, sans-serif',
    textposition: str = 'middle center',
    tekst_offset_x: float = None,
    tekst_offset_y: float = None):

    ## Voeg de lijn toe (zonder markers):
    # --------------------------------------
    fig = plot_lijn(
        fig=fig,
        xy_beginpunt=xy_beginpunt,
        xy_eindpunt=xy_eindpunt,
        color=color,
        line_dash=line_dash,
        line_width=line_width,
        tekst=tekst,
        tekst_size=tekst_size,
        tekst_color=tekst_color,
        tekst_family=tekst_family,
        textposition=textposition,
        tekst_offset_x=tekst_offset_x,
        tekst_offset_y=tekst_offset_y
    )

    ## Bereken hoek pijlpunten:
    # --------------------------------------
    hoek_radialen = np.arctan2(xy_eindpunt[1] - xy_beginpunt[1], xy_eindpunt[0] - xy_beginpunt[0])
    hoek_graden = np.degrees(hoek_radialen)

    ## Seed voor unieke naam:
    # --------------------------------------
    seed = np.random.rand()

    ## Voeg onderste pijlpunt toe:
    # --------------------------------------
    fig.add_trace(
        go.Scatter(
            x=[xy_beginpunt[0]],
            y=[xy_beginpunt[1]],
            name=f"onderste_pijlpunt_{seed}",
            mode='markers',
            marker=dict(
                color=color if marker_color is None else marker_color,
                angle=-hoek_graden - 90,
            ),
            showlegend=False,
        )
    )
    fig.update_traces(
        marker=dict(
            size=marker_size,
            symbol=marker_symbol,
            line=dict(width=2, color=marker_color_outline)
        ),
        selector=dict(name=f"onderste_pijlpunt_{seed}"),
        hoverinfo='none',
    )

    ## Voeg bovenste pijlpunt toe:
    # --------------------------------------
    if dubble_pijl:
        fig.add_trace(
            go.Scatter(
                x=[xy_eindpunt[0]],
                y=[xy_eindpunt[1]],
                name=f"bovenste_pijlpunt_{seed}",
                mode='markers',
                marker=dict(
                    color=color if marker_color is None else marker_color,
                    angle= -hoek_graden + 90,
                ),
                showlegend=False,
            )
        )
        fig.update_traces(
            marker=dict(
                size=marker_size,
                symbol=marker_symbol,
                line=dict(width=2, color=marker_color_outline)
            ),
            selector=dict(name=f"bovenste_pijlpunt_{seed}"),
            hoverinfo='none',
        )

    return fig