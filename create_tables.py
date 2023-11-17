import pandas as pd

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

def basic_field_table(gsid):
    field_columns = {
        'Nombre':'name',
        }
    f = spreadsheet_to_pandas('general',gsid)
    f = f.transpose()
    f.columns = f.iloc[0].replace(field_columns)
    f = f[1:].reset_index(drop=True)
    f = f[['name']]
    return f

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
    f = f[['weather_factor','rain_factor','dropcontrol_id','day_starttime','delay','weekday']]
    f['weatherstation'] = 1
    f['season']=1
    f['basic_field']=dbid
    return f


def zone_and_pump_tables(gsid, dbid):
    zone_columns = {
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
            'dist_emi':'transmitter_distance',
            'pp_real':'expected_real_precipitation', 
            'efi_riego':'irrigation_efficiency',
            'pondera_kc':'pondera_kc',
            'k_sat_mm':'k_sat', 
            'estrata':'soil_strata', 
            'caudal_nom':'expected_real_flow', 
            'superficie_sector':'surface',
            'productivo':'plantation_year', 
            'especie':'species', 
            'cuartel':'area_name',
            'rend/hect':'yield_kg',

        }
    
    f = spreadsheet_to_pandas('info_sectores',gsid)
    pump_table = f[['equipo','tranque_orig']].groupby(['equipo','tranque_orig']).count().reset_index()
    pump_table.rename(columns={'equipo':'name','tranque_orig':'reservoir'})
    pump_table['field'] = dbid
    
    f = f.rename(columns=zone_columns)
    f.drop(columns=['rendimiento', 'pondera_kc'])
    f['field'] = dbid
    f['species'] = 1
    return f, pump_table

def horizon_table(gsid):
    horizon_columns = {
        'equipo': 'pump', 
        'sector': 'zone', 
        'horizonte':'h_level', 
        'z_real':'z_real', 
        'cc_real':'cc_real', 
        'pmp_real':'pmp_real',
       'pedregosidad':'pedregosity', 
        }  
    f = spreadsheet_to_pandas('info_horizontes',gsid)
    f = f.rename(columns=horizon_columns)
    return f



