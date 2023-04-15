import pandas as pd
from campos import campos

def spreadsheet_to_pandas(sheet_name:str, id_spread:str):
        url = f'https://docs.google.com/spreadsheets/d/{id_spread}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
        df = pd.read_csv(url, engine='python')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        if sheet_name !='clima' and 'et0_real' in df.columns:
            print('Sheet not found')
            return None
        else:
            return df


def spreadsheet_melt(df:pd.DataFrame, value_name:str):
        df.rename(columns=lambda x: x.strip())
        df_melt = df.melt(id_vars='fecha', var_name='sector', value_name=f'{value_name}')
        df_melt['equipo'] = df_melt['sector'].str.split(' ',expand=True)[0]
        df_melt['sector'] = df_melt['sector'].str.split('_',expand=True)[1]
        df_melt = df_melt[['fecha','equipo','sector',f'{value_name}']]
        return df_melt

def fields_table(gsid, dbid):
    field_columns = {
        'Nombre':'name',
        'Factor estacion':'weather_factor',
        'Eficiencia precipitacion':'rain_factor',
        'Id dropcontrol':'dropcontrol_id',
        'Comienzo riego':'day_starttime',
        'Dia':'weekday',
        'Delay': 'delay',
    }

    f = spreadsheet_to_pandas('general',gsid)
    f = f.transpose()
    f.columns = f.iloc[0].replace(field_columns)
    f = f[1:].reset_index(drop=True)
    f['id'] = dbid
    return f

def real_irrigations_table(gsid, dbid):

    realirrigation_columns = { 
    'riego_bruto_progr':'scheduled_mm', 
    'volumen_progr':'scheduled_volume', 
    'pp_progr':'scheduled_precipitation', 
    'caudal_teorico':'theoretical_flow',
    'riego_bruto_hr_real':'duration', 
    'riego_bruto_real':'real_mm', 
    'riego_bruto_volumen':'real_volume', 
    'pp_real':'real_precipitation',
    'caudal_real': 'observed_flow',
    'id_real':'dropcontrol_id',
    'id_programado':'scheduled_id',
    }

    url = f'https://docs.google.com/spreadsheets/d/{gsid}/gviz/tq?tqx=out:csv&sheet=riego_real'
    reals = pd.read_csv(url, engine='python')
    reals['field_id'] = dbid
    reals['name'] = reals['field_id'].astype(str) + reals['equipo'].astype(str) + reals['sector'].astype(str)

    reals = reals.rename(columns=realirrigation_columns)
    return reals



def zone_and_pump_tables(gsid, dbid):
    zone_columns = {
            'index':'id',
            'equipo': 'pump',
            'sector': 'zone_number',
            'tipo_riego': 'irrigation_type',
            'id_wiseconn': 'dropcontrol_id',
            'coef_riego': 'irrigation_coef',
            'ancho_raices': 'root_size',
            'entre_hilera': 'row_sep',
            'sobre_hilera': 'row_over',
            'caudal_emisor': 'transmitter_flow',
            'late_plantas':'plant_laterality', 
            'dist_emi':'transmitter_dist',
            'pp_real':'expected_real_precipitation', 
            'efi_riego':'irrigation_efficiency',
            'pondera_kc':'pondera_kc',
            'k_sat_mm':'k_sat', 
            'estrata':'soil_strata', 
            'caudal_nom':'expected_real_flow', 
            'superficie_sector':'surface',
            'productivo':'plantation_year', 
            'especie':'species', 
        }
    
    f = spreadsheet_to_pandas('info_sectores',gsid)
    pump_table = f[['equipo','tranque_orig']].groupby(['equipo','tranque_orig']).count().reset_index()
    pump_table['field_id'] = dbid
    
    f = f.rename(columns=zone_columns)
    f['field_id'] = dbid
    f['name'] = f['field_id'].astype(str) + f['pump'].astype(str) + f['zone_number'].astype(str)
    
    return f, pump_table

def horizon_table(gsid, dbid):
    horizon_columns = {
        'equipo': 'pump', 
        'sector':'zone_number', 
        'horizonte':'horizon_number', 
        'z_real':'z_real', 
        'cc_real':'cc_real', 
        'pmp_real':'pmp_real',
       'pedregosidad':'pedregosity', 
       'd_a':'apparent_density', 
       'coef_ksat':'ksat_coef', 
       'coef_extr_etc':'extraction_coef'
        }
    
    f = spreadsheet_to_pandas('info_horizontes',gsid)
    f = f.rename(columns=horizon_columns)
    f['field_id'] = dbid
    f['name'] = f['field_id'].astype(str) + f['pump'].astype(str) + f['zone_number'].astype(str)
    
    return f
    
def kc_table(gsid, dbid):
    kc = spreadsheet_to_pandas('kc', gsid)
    kc = spreadsheet_melt(kc, 'kc')

    kc['field_id'] = dbid
    kc['value'] = kc['kc']
    kc = kc[~pd.isna(kc['value'])]
    kc['sector'] = kc['sector'].astype(int)
    kc['name'] = kc['field_id'].astype(str) + kc['equipo'].astype(str) + kc['sector'].astype(str)
    return kc#[['fecha','zone_name', 'value']]

def ur_table(gsid, dbid):
    ur = spreadsheet_to_pandas('ur', gsid)
    ur = spreadsheet_melt(ur, 'ur')

    ur['field_id'] = dbid
    ur['value'] = ur['ur']
    ur = ur[~pd.isna(ur['value'])]
    ur['sector'] = ur['sector'].astype(int)
    ur['name'] = ur['field_id'].astype(str) + ur['equipo'].astype(str) + ur['sector'].astype(str)
    return ur#[['fecha', 'field_id','zone_name', 'value']]

def inits_table(gsid, dbid):
    inicio = spreadsheet_to_pandas('inicio', gsid)
    inicio = spreadsheet_melt(inicio, 'inicio')

    inicio['field_id'] = dbid
    inicio['value'] = inicio['inicio']
    inicio['sector'] = inicio['sector'].astype(int) 
    inicio['name'] = inicio['field_id'].astype(str) + inicio['equipo'].astype(str) + inicio['sector'].astype(str)
    inicio = inicio[~pd.isna(inicio['value'])]
    return inicio[['fecha','name', 'value']]

def model_irrigations_table(gsid, dbid):
    models = spreadsheet_to_pandas('programas', gsid)

    models['field_id'] = dbid
    models['name'] = models['field_id'].astype(str) + models['equipo'].astype(str) + models['sector'].astype(str)
    #models['name']=models['name'].str.split('.').str[0]
    return models#[['fecha','zone_name']]

def weather_irrigations_table(gsid, dbid):
    clima = spreadsheet_to_pandas('clima', gsid)
    clima['field_id'] = dbid
    clima = pd.melt(clima,['fecha','field_id'],['et0_real','precipitacion'], var_name='type')
    return clima




