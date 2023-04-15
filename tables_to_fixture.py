import csv
import json
import os
from pathlib import Path

###  V1
def csv_to_fixture(csv_path, model_name, pk_field):
    """
    Convert a CSV file to a JSON fixture file.

    Args:
        csv_path (str or Path): The path to the CSV file.
        model_name (str): The name of the Django model being represented.
        pk_field (str): The name of the model field that is the primary key.

    Returns:
        A list of dictionaries, where each dictionary represents a single instance of the model.
    """
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        fixtures = []
        for row in reader:
            fixture = {
                'model': model_name,
                'pk': row[pk_field],
                'fields': {}
            }
            for field, value in row.items():
                if field != pk_field:
                    fixture['fields'][field] = value
            fixtures.append(fixture)
    return fixtures


def merge_fixtures(fixtures, output_path):
    """
    Merge a list of fixture dictionaries into a single fixture file.

    Args:
        fixtures (list): A list of fixture dictionaries.
        output_path (str or Path): The path to the output file.

    Returns:
        None
    """
    merged = {}
    for fixture in fixtures:
        model_name = fixture[0]['model']
        if model_name not in merged:
            merged[model_name] = []
        merged[model_name].extend(fixture)
    with open(output_path, 'w') as f:
        json.dump(merged, f, indent=4)


# Example usage
fixtures = [
    csv_to_fixture('./csvs/gota_rdb - WeatherStations.csv', 'gota_app.Weatherstation', 'id'),
    csv_to_fixture('./csvs/gota_rdb - Fields.csv', 'gota_app.Field', 'id'),
    csv_to_fixture('./csvs/gota_rdb - Pumps.csv', 'gota_app.Pump', 'id'),
    csv_to_fixture('./csvs/gota_rdb - Horizons.csv', 'gota_app.Horizon', 'id'),
    csv_to_fixture('./csvs/gota_rdb - Zones.csv', 'gota_app.Zone', 'id'),
    csv_to_fixture('./csvs/gota_rdb - KCs.csv', 'gota_app.KC', 'id'),
    csv_to_fixture('./csvs/gota_rdb - StationMeasures.csv', 'gota_app.StationMeasure', 'id'),
    csv_to_fixture('./csvs/gota_rdb - ModelIrrigations.csv', 'gota_app.ModelIrrigation', 'id'),
    csv_to_fixture('./csvs/gota_rdb - Thresholds.csv', 'gota_app.Threshold', 'id'),
    csv_to_fixture('./csvs/gota_rdb - WaterPoints.csv', 'gota_app.Waterpoint', 'id'),
    csv_to_fixture('./csvs/gota_rdb - Seasons.csv', 'gota_app.Season', 'id'),
    csv_to_fixture('./csvs/gota_rdb - Reservoirs.csv', 'gota_app.Reservoir', 'id'),
    
]
merge_fixtures(fixtures, 'db_content.json')



### V2

def csv_to_fixture_2(csv_file, model_name, pk_column):
    fixtures = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pk = row.pop(pk_column)
            fixture = {
                'model': model_name,
                'pk': pk,
                'fields': row,
            }
            fixtures.append(fixture)
    return json.dumps(fixtures, indent=2)

def combine_fixtures_2(fixture_dir):
    fixtures = []
    for filename in os.listdir(fixture_dir):
        if filename.endswith('.json'):
            with open(os.path.join(fixture_dir, filename), 'r') as f:
                fixtures.extend(json.load(f))
    return json.dumps(fixtures, indent=2)