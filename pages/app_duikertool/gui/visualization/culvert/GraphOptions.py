##############################################################################
## Created on Fri Aug 25 14:04:11 2023                                      ##
## Author: Niels van der Maaden                                             ##
##                                                                          ##
##                       -- Grafiekopties --                                ##
##                                                                          ##
## In dit bestand staan de grafiekopties voor all plots                     ##
##############################################################################

## Import packages:
# ============================================================================
import plotly.graph_objects as go

## Vooraanzicht:
# ======================================
def duiker_grafiekopties_vooraanzicht(fig, bok:float = None, title: str = None):
    fig.update_layout(
        title=title,
        # size figure
        width=2000,
        height=600,
    # Cancel possibility to zoom
        autosize=False,
        # Set background colour
        plot_bgcolor='#e1e0db',
        # Set axis options
        xaxis=dict(
            title="Breedte",
            showgrid=False,
            scaleanchor="y",
            scaleratio=1,
            fixedrange=True,
            # Axis line: line
            showline=True,
            linewidth=2,
            linecolor='black',
            zeroline=False,
            # Axis line: ticks
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            minor=dict(
                ticks='inside',
                ticklen=2.5,
                tickcolor='black',
                tickmode='auto',
                nticks=10,
                showgrid=False
            ),
        ),
        yaxis=dict(
            title='Hoogte' if bok == 0 else 'Hoogte m+NAP',
            showgrid=False,
            scaleanchor="x",
            scaleratio=1,
            fixedrange=True,
            # Axis line: line
            showline=True,
            linewidth=2,
            linecolor='black',
            zeroline=False,
            # Axis line: ticks
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            minor=dict(
                ticks='inside',
                ticklen=2.5,
                tickcolor='black',
                tickmode='auto',
                nticks=10,
                showgrid=False
            ),
        ),
        # Set legend layout
        legend=dict(
            # Define legend text size
            font=dict(
                size=32
            ),
            # Set legend symbol same size as legend text
            itemsizing='constant',
            traceorder="reversed"
        ),
    )
    return fig

## Zijaanzicht:
# ======================================
def duiker_grafiekopties_zijaanzicht(fig, bok:float = None, title: str = None):
    fig.update_layout(
        title=title,
        # size figure
        width=2000,
        height=600,
        # Cancel possibility to zoom
        autosize=False,
        # Set background colour
        plot_bgcolor='#e1e0db',
        # Set axis options
        xaxis=dict(
            title="Breedte",
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='black',
            zeroline=False,
            # Axis line: ticks
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            minor=dict(
                ticks='inside',
                ticklen=2.5,
                tickcolor='black',
                tickmode='auto',
                nticks=10,
                showgrid=False
            ),
        ),
        yaxis=dict(
            title='Hoogte' if bok == 0 else 'Hoogte m+NAP',
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='black',
            zeroline=False,
            # Axis line: ticks
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            minor=dict(
                ticks='inside',
                ticklen=2.5,
                tickcolor='black',
                tickmode='auto',
                nticks=10,
                showgrid=False
            ),
            mirror='all',
        ),
        # Set legend layout
        legend=dict(
            # Define legend text size
            font=dict(
                size=32
            ),
            # Set legend symbol same size as legend text
            itemsizing='constant',
            traceorder="reversed"
        ),
    )

    return fig