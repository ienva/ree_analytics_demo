# REE API Demo

This project demonstrates a complete data pipeline for collecting, processing, and analyzing real-time and historical energy data from the Spanish electricity system (REE/ESIOS API). The pipeline is designed for analytics, reporting, and dashboarding using Tinybird as the backend.

## Overview
- **Data is fetched** from the ESIOS (Red Eléctrica de España) API using a Python application.
- **Data is processed and sent** to Tinybird, a real-time data platform for analytics.
- **Tinybird resources** (datasources, materializations, endpoints) structure and expose the data for dashboards or further analysis.

## Project Structure

- [`ree_data_tracker/`](ree_data_tracker/README.md): Python code for fetching, processing, and sending data.
  - Fetches data from ESIOS API.
  - Processes and formats the data.
  - Sends data to Tinybird.
  - Includes unit tests and configuration.
- [`tinybird/`](tinybird/README.md): Tinybird backend resources.
  - Datasources: Raw and processed tables.
  - Materializations: SQL nodes for filtering/aggregating data.
  - Endpoints: API pipes for analytics and dashboards.

## How It Works
1. **Python app** (`ree_data_tracker/`) fetches and processes energy data from ESIOS.
2. **Processed data** is sent to Tinybird (`landing_ds` datasource).
3. **Tinybird** materializes and exposes the data through endpoints for easy integration with BI tools or custom dashboards.

## Getting Started
- See [`ree_data_tracker/README.md`](ree_data_tracker/README.md) for setup, running, and testing the Python pipeline.
- See [`tinybird/README.md`](tinybird/README.md) for details on the Tinybird backend and available endpoints.

## Use Cases
- Real-time and historical energy analytics
- Dashboarding and reporting
- Data engineering and pipeline demonstration

---

For more details, check the README in each subfolder. 