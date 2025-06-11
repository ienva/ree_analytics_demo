import csv
import json
import os
from pathlib import Path

def convert_value(value, key):
    if key in ['geo_id', 'metric_id']:
        return int(value)
    elif key == 'value':
        try:
            float_val = float(value)
            return int(float_val) if float_val.is_integer() else float_val
        except (ValueError, TypeError):
            return value
    return value

def convert_csv_to_json(csv_file):
    # Read CSV file
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            # Convert numeric values
            converted_row = {
                key: convert_value(value, key)
                for key, value in row.items()
            }
            data.append(converted_row)
    
    # Create JSON filename
    json_file = csv_file.with_suffix('.json')
    
    # Write JSON file in NDJSON format (one object per line)
    with open(json_file, 'w') as f:
        for row in data:
            f.write(json.dumps(row) + '\n')

def main():
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    # Find all CSV files in the directory
    csv_files = list(script_dir.glob('*.csv'))
    
    # Convert each CSV file to JSON
    for csv_file in csv_files:
        print(f"Converting {csv_file.name} to JSON...")
        convert_csv_to_json(csv_file)
        print(f"Created {csv_file.stem}.json")

if __name__ == '__main__':
    main() 