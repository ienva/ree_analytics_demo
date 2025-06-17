from fetcher.fetcher import get_rt_demand_peninsular, get_rt_demand_nacional, get_generation, get_renewable_non_generation, get_spot_costs, get_estimated_generation
from sender.tinybird_sender import send_to_tinybird
import time
import datetime as dt
from config.logging_config import setup_logger

# Initialize logger with Tinybird handler
logger = setup_logger('main', send_callback=send_to_tinybird)

while True:
    try:
        now_time = dt.datetime.now().time()
        logger.info("Starting data collection cycle")
        
        data_demand = get_rt_demand_peninsular()
        data_national_demand = get_rt_demand_nacional()
        data_generation = get_generation()
        data_estimated_generation = get_estimated_generation()
        time.sleep(2)
        renewable_generation = get_renewable_non_generation()
        data_spot_costs = []
        
        if now_time > dt.time(14, 30) and now_time < dt.time(14, 38):
            logger.info("Fetching spot costs data")
            data_spot_costs = get_spot_costs()
            
        payload_landing = data_demand + data_generation + data_national_demand + renewable_generation + data_estimated_generation
        logger.info(f"Sending {len(payload_landing)} records to Tinybird landing_ds")
        send_to_tinybird(payload_landing, 'landing_ds')
        
        if data_spot_costs:
            logger.info(f"Sending {len(data_spot_costs)} spot cost records to Tinybird landing_ds")
            send_to_tinybird(data_spot_costs, 'landing_ds')
            
        logger.info("Data collection cycle completed successfully")
        time.sleep(300)
        
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}", exc_info=True)
        time.sleep(60)  # Wait a minute before retrying on error
