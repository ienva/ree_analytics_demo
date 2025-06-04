from datetime import datetime, timedelta
import pytz
from fetcher import fetcher
from sender.tinybird_sender import send_to_tinybird
from config.logging_config import setup_logger

logger = setup_logger('backfill')

# Helper to get UTC datetimes for the last 24 hours
now = datetime.now(pytz.timezone('UTC')).replace(second=0, microsecond=0)
start = now - timedelta(hours=24)

# Format for API
start_str = start.strftime("%Y-%m-%dT%H:%M:%SZ")
end_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")

# Indicator groups (from fetcher.py logic)
indicator_groups = {
    'peninsular_demand': [1293],
    'national_demand': [2037, 2052, 2053, 2054],
    'generation': [2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051],
    'renewable_non_generation': [10351, 10352, 10353, 10354],
    'estimated_generation': [542, 543, 10034],
    'spot_costs': [600],
}

def fetch_and_send(indicator_ids, datasource):
    all_data = []
    for indicator_id in indicator_ids:
        params = {'start_date': start_str, 'end_date': end_str}
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
    logger.info("Starting backfill process for the last 24 hours")
    logger.info(f"Time range: {start_str} to {end_str}")
    
    try:
        fetch_and_send(indicator_groups['peninsular_demand'], 'landing_ds')
        fetch_and_send(indicator_groups['national_demand'], 'landing_ds')
        fetch_and_send(indicator_groups['generation'], 'landing_ds')
        fetch_and_send(indicator_groups['renewable_non_generation'], 'landing_ds')
        fetch_and_send(indicator_groups['estimated_generation'], 'landing_ds')
        fetch_and_send(indicator_groups['spot_costs'], 'landing_ds')
        
        logger.info("Backfill process completed successfully")
    except Exception as e:
        logger.error(f"Error during backfill process: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main() 