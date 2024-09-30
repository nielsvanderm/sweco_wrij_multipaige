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
import os
import plotly.graph_objects as go

dir = os.path.dirname(os.path.abspath(__file__))

## Maaiveld arcering:
# ======================================
def plot_arcering_maaiveld(fig,
                           x_left: float = None,
                           x_centre: float = None,
                           y_top: float = None,
                           size: float = None,
                           size_x: float = None,
                           size_y: float = None,
                           rotation: float = 0,
                           color: str = 'black'):

    ## Initalisatie:
    # --------------------------------------
    maaiveld_arcering = pd.read_csv(f"{dir}/maaiveld/maaiveld_arcering.csv", sep=';')
    # Roteer de arcering (0=horizontaal)
    # maaiveld_arcering = rotate_coordinates(maaiveld_arcering, rotation)

    # Verander grootte
    if size:
        maaiveld_arcering *= size
    if size_x or size_y:
        maaiveld_arcering['x'] *= size_x
    if size_y:
        maaiveld_arcering['y'] *= size_y


    ## Pas xy aan om arcering te plaatsen:
    # --------------------------------------
    if x_centre:
        x_max = maaiveld_arcering['x'].max()
        maaiveld_arcering['x'] += x_centre - (x_max/2)
    elif x_left:
        maaiveld_arcering['x'] += x_left
    maaiveld_arcering['y'] += y_top

    ## Plot maaiveld arcering:
    # --------------------------------------
    fig.add_trace(go.Scatter(
        x=list(maaiveld_arcering['x']),
        y=list(maaiveld_arcering['y']),
        line=dict(width=1.0, color=color),
        hoverinfo='none',
        showlegend=False,
    ))

    return fig

## Waterlijn arcering:
# ======================================
def plot_arcering_waterlijn(fig,
                           x_left: float = None,
                           x_centre: float = None,
                           y_top: float = None,
                           size: float = None,
                           size_x: float = None,
                           size_y: float = None,
                           color: str = 'black'):

    ## Initalisatie:
    # --------------------------------------
    waterlijn_arcering = pd.read_csv(f"{dir}/waterlijn/waterlijn_arcering.csv", sep=';')

    # Verander grootte
    if size:
        waterlijn_arcering *= size
    if size_x or size_y:
        waterlijn_arcering['x'] *= size_x
    if size_y:
        waterlijn_arcering['y'] *= size_y

    ## Pas xy aan om arcering te plaatsen:
    # --------------------------------------
    if x_centre:
        x_max = waterlijn_arcering['x'].max()
        waterlijn_arcering['x'] += x_centre - (x_max/2)
    elif x_left:
        waterlijn_arcering['x'] += x_left
    waterlijn_arcering['y'] += y_top

    ## Plot maaiveld arcering:
    # --------------------------------------
    fig.add_trace(
        go.Scatter(
            x=waterlijn_arcering['x'][0:2],
            y=waterlijn_arcering['y'][0:2],
            mode='lines',
            line=dict(width=2, color=color),
            hoverinfo='none',
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=waterlijn_arcering['x'][2:4],
            y=waterlijn_arcering['y'][2:4],
            mode='lines',
            line=dict(width=2, color=color),
            hoverinfo='none',
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=waterlijn_arcering['x'][4:],
            y=waterlijn_arcering['y'][4:],
            mode='lines',
            line=dict(width=2, color=color),
            hoverinfo='none',
            showlegend=False,
        )
    )

    return fig