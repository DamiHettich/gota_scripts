import pandas as pd
from campitos import campos
from create_tables import *


for i, field in enumerate(campos):
    print(f'working on {field}')
    id_db = campos[field]['id']
    id = campos[field]['spreadsheet_id']
    if i == 0:
        fields = fields_table(id, id_db)
        z, p = zone_and_pump_tables(id, id_db)
        h = horizon_table(id, id_db)
    else:
        fields2 = fields_table(id, id_db)
        fields = pd.concat([fields,fields2])
        z2, p2 = zone_and_pump_tables(id, id_db)
        z = pd.concat([z, z2])
        p = pd.concat([p, p2])
        h2 = horizon_table(id, id_db)
