import pandas as pd
from campos import campos
from create_tables import *


for i, field in enumerate(campos):
    print(f'working on {field}')
    id_db = campos[field]['id']
    id = campos[field]['spreadsheet_id']
    if i == 0:
        fields = fields_table(id, id_db)
        z, p = zone_and_pump_tables(id, id_db)
        h = horizon_table(id, id_db)
        k = kc_table(id, id_db)
        inits = inits_table(id, id_db)
        u = ur_table(id, id_db)
        m = model_irrigations_table(id, id_db)
        f = weather_irrigations_table(id, id_db)
    else:
        fields2 = fields_table(id, id_db)
        fields = pd.concat([fields,fields2])
        z2, p2 = zone_and_pump_tables(id, id_db)
        z = pd.concat([z, z2])
        p = pd.concat([p, p2])
        h2 = horizon_table(id, id_db)
        h = pd.concat([h,h2])
        k2 = kc_table(id, id_db)
        k = pd.concat([k,k2])
        inits2 = inits_table(id, id_db)
        inits = pd.concat([inits,inits2])
        u2 = ur_table(id, id_db)
        u = pd.concat([u, u2])
        m2 = model_irrigations_table(id, id_db)
        m = pd.concat([m,m2])
        f2 = weather_irrigations_table(id, id_db)
        f = pd.concat([f,f2])
