import pandas as pd
from datetime import datetime

def define_metadata(
    titel: str = None,
    gebruikersnaam: str = None,
    periode_aangevraagd_start:str = '01-01-1800',
    periode_aangevraagd_end:str = str(datetime.now().strftime("%d-%m-%Y")),
    gegevens_beschikbaar_start:str = None,
    gegevens_beschikbaar_end:str = None,
    datum:str = str(datetime.now().strftime("%d-%m-%Y")),

    locatie:str = None,
    filternummer:int = 1,
    externe_aanduiding:str = None,
    xcordinaat:float = 0,
    ycordinaat:float = 0,
    mv_tov_nap: float = None,
    datum_mv:str = None,
    datum_start:str = None,
    datum_end:str = None,
    mp_tov_nap:float = None,
    mp_tov_mv:float = None,
    filter_boven:float = None,
    filter_onder:float = None,
    **kwargs
):

    metadata = [
        # These values need to be underneath each other in separate rows 
        {
            'col_1': 'Titel', 
            'col_2': titel},
        {
            'col_1': 'Gebruikersnaam', 
            'col_2': gebruikersnaam},
        {
            'col_1': 'Periode aangevraagd', 
            'col_2': pd.to_datetime(periode_aangevraagd_start).strftime('%d-%m-%Y'), 
            'col_3': 'tot:', 
            'col_4': pd.to_datetime(periode_aangevraagd_end).strftime('%d-%m-%Y')},
        {
            'col_1': 'Gegevens beschikbaar', 
            'col_2': pd.to_datetime(gegevens_beschikbaar_start).strftime('%d-%m-%Y'), 
            'col_3': 'tot:', 
            'col_4': pd.to_datetime(gegevens_beschikbaar_end).strftime('%d-%m-%Y')},
        {
            'col_1': 'Datum', 
            'col_2': pd.to_datetime(datum).strftime('%d-%m-%Y')},
        {
            'col_1': 'Referentie', 
            'col_2': 'NAP'},
        {},    
        {
            'col_1': 'NAP', 
            'col_2': 'Normaal Amsterdams Peil'},
        {
            'col_1': 'MV', 
            'col_2': 'Maaiveld'},
        {
            'col_1': 'MP', 
            'col_2': 'Meetpunt'},
        {},

        # These values need to be next to each other in separate columns
        {
            'col_1': 'Locatie',
            'col_2': 'Filternummer',
            'col_3': 'Externe aanduiding',
            'col_4': 'X-coordinaat',
            'col_5': 'Y-coordinaat',
            'col_6': 'Maaiveld (cm t.o.v. NAP)',
            'col_7': 'Datum maaiveld gemeten',
            'col_8': 'Startdatum',
            'col_9': 'Einddatum',
            'col_10': 'Meetpunt (cm t.o.v. NAP)',
            'col_11': 'Meetpunt (cm t.o.v. MV)',
            'col_12': 'Bovenkant filter (cm t.o.v. NAP)',
            'col_13': 'Onderkant filter (cm t.o.v. NAP)',
        },
        {
            'col_1': locatie,
            'col_2': filternummer,
            'col_3': externe_aanduiding,
            'col_4': xcordinaat,
            'col_5': ycordinaat,
            'col_6': mv_tov_nap,
            'col_7': pd.to_datetime(datum_mv).strftime('%d-%m-%Y'),
            'col_8': pd.to_datetime(datum_start).strftime('%d-%m-%Y'),
            'col_9': pd.to_datetime(datum_end).strftime('%d-%m-%Y'),
            'col_10': mp_tov_mv,
            'col_11': mp_tov_nap,
            'col_12': filter_boven,
            'col_13': filter_onder,
        },
        {},

        # These are the headers for the time series
        {
            'col_1': 'Locatie',
            'col_2': 'Filternummer',
            'col_3': 'Peildatum',
            'col_4': 'Stand (cm t.o.v. MP)',
            'col_5': 'Stand (cm t.o.v. MV)',
            'col_6': 'Stand (cm t.o.v NAP)',
            'col_7': 'Bijzonderheid',
            'col_8': 'Opmerking',    
        },
    ]

    return metadata

def define_time_series(
    import_df:pd.DataFrame = None,
    locatie:str = None,
    filternummer:str = 1,
    mp_tov_nap:float = None,
    mp_tov_mv:float = None,
    **kwargs
):
    # Define name of well from import file only when none is given
    locatie = locatie if locatie else import_df.columns[2].split('/')[0]

    time_series = {
        # Fill rows with single value
        'col_1': locatie,
        'col_2': filternummer,
        # Fill rows with values from import file
        'col_3': pd.to_datetime(import_df['Date']).dt.strftime('%d-%m-%Y'),
        # Calculate rows. Select third colomn, only apply logic if metadata is present
        'col_4': mp_tov_nap - import_df.iloc[:, 2]  if mp_tov_nap else None,
        'col_5': mp_tov_mv - import_df.iloc[:, 2]  if mp_tov_mv else None,
        # Fill rows with values from import file
        'col_6': import_df.iloc[:, 2]
    }

    return time_series

def construct_exportfile(**kwargs):
    # Filter de kwargs om dubbele argumenten te verwijderen
    filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ['gegevens_beschikbaar_start', 'gegevens_beschikbaar_end', 'locatie']}

    # Construct time series, returns a dict
    time_series = define_time_series(**kwargs)

    # Construct metadata, returns a dict
    metadata = define_metadata(
        gegevens_beschikbaar_start=time_series['col_3'].iloc[0],
        gegevens_beschikbaar_end=time_series['col_3'].iloc[-1],
        locatie=time_series['col_1'],
        **filtered_kwargs
    )

    export_df = pd.concat([pd.DataFrame(metadata), pd.DataFrame(time_series)], ignore_index=True)

    return export_df