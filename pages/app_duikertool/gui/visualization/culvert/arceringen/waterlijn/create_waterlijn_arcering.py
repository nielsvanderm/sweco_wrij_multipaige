##############################################################################
## Created on Fri Aug 25 14:04:11 2023                                      ##
## Author: Niels van der Maaden                                             ##
##                                                                          ##
##                -- create waterlijn Arcering --                           ##
##                                                                          ##
## Dit bestand maakt de csv-bestand dat de waterlijn arcering representeerd ##
##############################################################################

## Import packages:
# ============================================================================
import pandas as pd
import plotly.graph_objects as go

## Waterlijn arcering:
# ======================================
x = [
    0, 1,
    1/6, 5/6,
    1/3, 2/3,
]

y = [
    -0.025, -0.025,
    -0.050, -0.050,
    -0.075, -0.075,
]

df = pd.DataFrame({'x': x, 'y': y})
df.to_csv(sep=';', path_or_buf='waterlijn_arcering.csv', index=False)


fig = go.Figure()

# Voeg de eerste lijn toe
fig.add_trace(go.Scatter(x=x[0:2], y=y[0:2], mode='lines', line=dict(width=2, color='black')))

# Voeg de tweede lijn toe
fig.add_trace(go.Scatter(x=x[2:4], y=y[2:4], mode='lines', line=dict(width=2, color='black')))

# Voeg de derde lijn toe
fig.add_trace(go.Scatter(x=x[4:], y=y[4:], mode='lines',line=dict(width=2, color='black')))

fig.show()