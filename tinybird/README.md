# Tinybird Resources

This folder contains the Tinybird resources used by the REE Data Tracker app. These resources structure, process, and expose energy data fetched from the ESIOS API.

## Structure
- **datasources/**: Raw and processed data tables (e.g., landing_ds, generation_mv)
- **materializations/**: SQL nodes that filter and transform data from datasources for analytics
- **endpoints/**: API endpoints (pipes) that expose processed data for use in dashboards or external apps

---

## Main Datasource

### `landing_ds.datasource`
- **Purpose**: Main landing table for all electric indicators ingested from ESIOS.
- **Schema**: Includes timestamps, geo info, metric id/name, and value.

---

## Materializations
Materializations filter and aggregate data from `landing_ds` into specialized views:

- **estimated_generation_mv**: Estimated generation metrics (IDs: 542, 543, 10034)
- **daily_spot_mv**: Daily spot price (ID: 600)
- **renewable_generation_mv**: Renewable/non-renewable generation (IDs: 10351, 10352, 10353, 10354)
- **national_demand_mv**: National demand (IDs: 2037, 2052, 2053, 2054)
- **peninsular_demand_mv**: Peninsular demand (ID: 1293)
- **generation_mv**: Generation by technology (IDs: 2038–2051)

---

## Endpoints
Endpoints expose processed data for analytics and dashboards:

- **generation_by_technology_perc.pipe**: Percentage of generation by technology (last 6 hours)
- **estimated_generacion.pipe**: Estimated generation timeseries
- **daily_spot_prices.pipe**: Spot prices timeseries
- **renewable_energy_perc.pipe**: Percentage of renewable energy generation
- **peninsular_demand_ep.pipe**: Peninsular demand timeseries
- **national_demand_ep.pipe**: National demand timeseries
- **generation_ep.pipe**: Generation by technology timeseries

Each endpoint is defined as a Tinybird pipe and can be queried via HTTP for integration with BI tools or custom dashboards.

---

## How Data Flows
1. **Data is ingested** into `landing_ds` from the Python app.
2. **Materializations** filter and aggregate the data into specialized views.
3. **Endpoints** expose the processed data for analytics and visualization.

---

For more details, see the SQL and schema in each resource file. 