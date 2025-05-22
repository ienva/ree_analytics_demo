from fetcher.fetcher import get_rt_demand_peninsular, get_rt_demand_nacional, get_generation, get_renewable_non_generation, get_spot_costs
from sender.tinybird_sender import send_to_tinybird
import time
import datetime as dt
import pytz


now_time = dt.datetime.now().time()

while True:
    data_demand = get_rt_demand_peninsular()
    data_national_demand = get_rt_demand_nacional()
    data_generation = get_generation()
    time.sleep(2)
    renewable_generation = get_renewable_non_generation()
    data_spot_costs = []
    if now_time > dt.time(14, 30) and now_time < dt.time(14, 38):
        data_spot_costs = get_spot_costs()
    payload_landing = data_demand + data_generation + data_national_demand + renewable_generation
    send_to_tinybird(payload_landing, 'landing_ds')
    send_to_tinybird(data_spot_costs, 'landing_ds')
    time.sleep(300)
