##############################################################################
## Created on Fri Aug 25 14:04:11 2023                              		##
## Author: Niels van der Maaden              								##
##                                  										##
##                          -- DuikerTool --            					##
##                             												##
## Dit bestand maakt de duikerberekeningen debiet en opstuwing              ##
##############################################################################

## Import packages:
# ============================================================================
import numpy as np
from pydantic import BaseModel
import logging

# Obtain a logger for this module
logger = logging.getLogger(__name__)

## Culvert paramaters
# ======================================
'''Calculates the wetted area (m²) of the culvert. It computes the area of the 
soil and air pocket inside the culvert. The wetted area is then determined 
by subtracting the soil and air pocket areas from the total culvert area.'''
def calculate_wetted_area(
    culvert_diameter:float = None,
    soil_column_culvert:float = None,
    air_column_culvert:float = None):

    # Radius
    radius = culvert_diameter * 0.5

    # Angles of the missing parts in radians
    theta_soil = 2 * np.arccos((radius - soil_column_culvert) / radius)
    theta_air = 2 * np.arccos((radius - air_column_culvert) / radius)

    # Area of ​​the entire culvert
    area_culvert = np.pi * radius ** 2

    # Area of the segments
    area_segment_soil = 0.5 * radius ** 2 * (theta_soil - np.sin(theta_soil))
    area_segment_air = 0.5 * radius ** 2 * (theta_air - np.sin(theta_air))

    # Area of ​​the culvert without the segments
    wetted_area = area_culvert - area_segment_soil - area_segment_air

    logger.debug(f"Wettet area culvert = {round(wetted_area, 2)}")

    return wetted_area

'''Calulates the wetted perimeter [m]. It computes the perimeter of the 
soil and air pocket inside the culvert. The wetted perimeter is then determined 
by subtracting the soil and air pocket perimeters from the total culvert perimeter.'''
def calculate_wetted_perimeter(
    culvert_diameter:float = None,
    soil_column_culvert:float = None,
    air_column_culvert:float = None):
    
    # Radius
    radius = culvert_diameter * 0.5

    # Angles of the missing parts in radians
    theta_soil = 2 * np.arccos((radius - soil_column_culvert) / radius)
    theta_air = 2 * np.arccos((radius - air_column_culvert) / radius)

    # Perimeter of the entier culvert
    perimeter_culvert = 2 * np.pi * radius

    # Perimeter of ​​the culvert without the segments
    wetted_perimeter = perimeter_culvert - (radius * theta_soil) - (radius * theta_air)

    logger.debug(f"Wetted perimeter = {round(wetted_perimeter, 2)}")

    return wetted_perimeter

def calculate_hydraulic_radius(
    wetted_area:float = None,
    wetted_perimeter:float = None):

    hydraulic_radius = wetted_area / wetted_perimeter
    logger.debug(f"Hydraulic radius = {round(hydraulic_radius, 2)}")
    return hydraulic_radius

'''Calculates the air column in the culvert. Uses the max() function
to prevent value lower than zero'''
def calculate_air_column_culvert(
    culvert_diameter:float = None,
    soil_column_culvert:float = None,
    water_column_upstream:float = None):

    air_column_culvert = max(culvert_diameter - soil_column_culvert - water_column_upstream, 0)
    logger.debug(f"Air fraction culvert = {round(air_column_culvert, 2)}")
    return air_column_culvert

## Friction loss 
# =======================================
def calculate_loss_coefficient(
    inlet_flow_resistance:float = None,
    friction_loss: float = None,
    exit_loss:float = None,
    bend_loss_coefficient:float = None,
    n_bends:int = None):

    loss_coefficient = 1 / (inlet_flow_resistance + friction_loss + exit_loss + (n_bends * bend_loss_coefficient))**0.5
    logger.debug(f"Loss coefficient = {round(loss_coefficient, 4)}")
    return loss_coefficient

def calculate_roughness_coefficient(
    manning_roughness_coefficient:float = None,
    hydraulic_radius:float = None):

    roughness_coefficient = manning_roughness_coefficient*hydraulic_radius**(1/6)
    logger.debug(f"Roughness coefficient = {round(roughness_coefficient, 4)}")
    return roughness_coefficient

def calculate_friction_loss(
    culvert_length:float = None,
    roughness_coefficient:float = None,
    hydraulic_radius:float = None):
    
    gravity_acceleration = 9.81
    friction_loss = (2*gravity_acceleration*culvert_length)/(roughness_coefficient**2*hydraulic_radius)
    logger.debug(f"Friction loss = {round(friction_loss, 4)}")
    return friction_loss

def calculate_exit_loss(
    n_parallel_culverts:int = None,
    wetted_area_culvert:float = None,
    wetted_area_channel_downstream:float = None,
    outlet_shape_coefficient:float = None):

    alpha = wetted_area_culvert / wetted_area_channel_downstream
    exit_loss = (1-n_parallel_culverts*alpha)**2*outlet_shape_coefficient
    logger.debug(f"Exit loss = {round(exit_loss, 4)}")
    return exit_loss

## Result
# =======================================
def calculate_backwater(
    loss_coefficient:float = None,
    discharge:float = None,
    wetted_area_culvert:float = None):

    gravity_acceleration = 9.81
    backwater = (1/(loss_coefficient**2*2*gravity_acceleration)) * (discharge**2*wetted_area_culvert**-2)
    logger.debug(f"Backwater = {round(backwater, 4)}")
    return backwater

def calculate_discharge(
    loss_coefficient:float = None,
    wetted_area_culvert:float = None,
    backwater:float = None):

    gravity_acceleration = 9.81
    discharge = loss_coefficient * wetted_area_culvert * np.sqrt(2*gravity_acceleration*backwater)
    logger.debug(f"Discharge = {round(discharge, 4)}")
    return discharge

def calculate_flow_velocity(
    discharge:float = None,
    wetted_area_culvert:float = None):
    flow_velocity = discharge/wetted_area_culvert
    logger.debug(f"Flow velocity = {round(flow_velocity, 2)}")
    return flow_velocity

def culvert_calculator(
    
    ## Calculation option ['discharge', 'backwater']
    #-------------------------------
    calculate:str = 'discharge',

    ## Culvert parameters
    #-------------------------------
    culvert_diameter:float = None,
    culvert_length:float = None,
    culvert_slope:float = None,

    ## Randvoorwaarden
    #-------------------------------
    soil_column_culvert:float = None,
    water_column_upstream:float = None,
    water_column_downstream:float = None,
    backwater:float = None,
    discharge:float = None,
    wetted_area_channel_downstream:float= None,

    ## Friction
    #-------------------------------
    manning_roughness_coefficient:float = None,
    inlet_flow_resistance:float = None,
    n_parallel_culverts:int = 1,
    outlet_shape_coefficient:float = None,
    bend_loss_coefficient:float = None,
    n_bends: int = None,
    
    **kwargs
):
    ## Forcings
    #-------------------------------    
    # Here perhaps some adjustment is neccacery 
    if not culvert_slope:
        culvert_slope = 0.01 * culvert_length
    if calculate == 'discharge':
        if not backwater:
            backwater = water_column_upstream - water_column_downstream - culvert_slope
        if not water_column_upstream:
            print('a')
    # elif calculate == 'backwater':
    #     if not water_column_downstream:
    #         water_column_downstream = 0

    ## Calculate paramaters
    #-------------------------------
    air_column_culvert = calculate_air_column_culvert(
        culvert_diameter=culvert_diameter,
        soil_column_culvert=soil_column_culvert,
        water_column_upstream=water_column_upstream,
    )

    wetted_area = calculate_wetted_area(
        culvert_diameter=culvert_diameter,
        soil_column_culvert=soil_column_culvert,
        air_column_culvert=air_column_culvert,
    )

    wetted_perimeter = calculate_wetted_perimeter(
        culvert_diameter=culvert_diameter,
        soil_column_culvert=soil_column_culvert,
        air_column_culvert=air_column_culvert,        
    )

    hydraulic_radius = calculate_hydraulic_radius(
        wetted_area=wetted_area,
        wetted_perimeter=wetted_perimeter,
    )

    roughness_coefficient = calculate_roughness_coefficient(
        manning_roughness_coefficient=manning_roughness_coefficient,
        hydraulic_radius=hydraulic_radius
    )

    friction_loss = calculate_friction_loss(
        culvert_length=culvert_length,
        roughness_coefficient=roughness_coefficient,
        hydraulic_radius=hydraulic_radius,
    )

    exit_loss = calculate_exit_loss(
        n_parallel_culverts=n_parallel_culverts,
        wetted_area_culvert=wetted_area,
        wetted_area_channel_downstream=wetted_area_channel_downstream,
        outlet_shape_coefficient=outlet_shape_coefficient,
    )

    loss_coefficient = calculate_loss_coefficient(
        inlet_flow_resistance=inlet_flow_resistance,
        friction_loss=friction_loss,
        exit_loss=exit_loss,
        bend_loss_coefficient=bend_loss_coefficient,
        n_bends=n_bends,
    )

    ## Calculate result
    #-------------------------------
    if calculate == 'discharge':
        discharge = calculate_discharge(
            loss_coefficient=loss_coefficient,
            backwater=backwater,
            wetted_area_culvert=wetted_area,
        )
    elif calculate == 'backwater':
        backwater = calculate_backwater(
        loss_coefficient=loss_coefficient,
        discharge=discharge,
        wetted_area_culvert=wetted_area,
    )
    else:
        logger.error(f"Wrong imput for culvert_calculator: calculate! Options are ['discharge', 'backwater']")
        raise ValueError(f"Wrong imput for culvert_calculator: calculate! Options are ['discharge', 'backwater']")

    flow_velocity = calculate_flow_velocity(
        discharge=discharge,
        wetted_area_culvert=wetted_area,
    )

    ## Return result
    #-------------------------------
    return dict(
        # Given paramaters
        calculate=calculate,
        culvert_diameter=culvert_diameter,
        culvert_length=culvert_length,
        culvert_slope=culvert_slope,
        soil_column_culvert=soil_column_culvert,
        water_column_upstream=water_column_upstream,
        water_column_downstream=water_column_downstream,
        wetted_area_channel_downstream=wetted_area_channel_downstream,
        manning_roughness_coefficient=manning_roughness_coefficient,
        inlet_flow_resistance=inlet_flow_resistance,
        n_parallel_culverts=n_parallel_culverts,
        outlet_shape_coefficient=outlet_shape_coefficient,
        bend_loss_coefficient=bend_loss_coefficient,
        n_bends=n_bends,

        # Calculated results
        air_column_culvert=air_column_culvert,
        wetted_area=wetted_area,
        wetted_perimeter=wetted_perimeter,
        hydraulic_radius=hydraulic_radius,
        roughness_coefficient=roughness_coefficient,
        friction_loss=friction_loss,
        exit_loss=exit_loss,
        loss_coefficient=loss_coefficient,
        discharge=discharge,
        backwater=backwater,
        flow_velocity=flow_velocity,
    )