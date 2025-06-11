from datetime import datetime
import pytz
import argparse
from fetcher import fetcher
from sender.tinybird_sender import send_to_tinybird
from config.logging_config import setup_logger

logger = setup_logger('backfill_date_range')

# Indicator groups (from fetcher.py logic)
indicator_groups = {
    'peninsular_demand': [1293],
    'national_demand': [2037, 2052, 2053, 2054],
    'generation': [2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051],
    'renewable_non_generation': [10351, 10352, 10353, 10354],
    'estimated_generation': [542, 543, 10034],
    'spot_costs': [600],
}

def parse_date(date_str):
    """Parse date string in format YYYY-MM-DD to UTC datetime"""
    try:
        # Parse the input date and set it to midnight UTC
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return pytz.UTC.localize(date)
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")

def fetch_and_send(start_date, end_date, indicator_ids, datasource):
    """Fetch and send data for a specific date range and indicators"""
    all_data = []
    for indicator_id in indicator_ids:
        params = {
            'start_date': start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'end_date': end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        data = fetcher.fetch_data(indicator_id, params)
        if data:
            processed = fetcher.processing_data(data)
            all_data.extend(processed)
    
    if all_data:
        logger.info(f"Sending {len(all_data)} records to Tinybird ({datasource})")
        send_to_tinybird(all_data, datasource)
    else:
        logger.warning(f"No data to send for {datasource}")

def main():
    parser = argparse.ArgumentParser(description='Backfill REE data for a specific date range')
    parser.add_argument('start_date', help='Start date in YYYY-MM-DD format')
    parser.add_argument('end_date', help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    try:
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date)

        if end_date < start_date:
            logger.error("End date must be after start date")
            return

        logger.info(f"Starting backfill from {start_date} to {end_date}")

        # Process each indicator group
        for group_name, indicator_ids in indicator_groups.items():
            logger.info(f"Processing {group_name} indicators")
            fetch_and_send(start_date, end_date, indicator_ids, 'landing_ds')

        logger.info("Backfill completed successfully")

    except ValueError as e:
        logger.error(f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main() 