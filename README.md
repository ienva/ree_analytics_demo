# REE API Demo

This project demonstrates the integration between REE's API, Tinybird, and Grafana for real-time energy data monitoring and visualization.

## Overview
- **Data is fetched** from the ESIOS (Red Eléctrica de España) API using a Python application.
- **Data is processed and sent** to Tinybird, a real-time data platform for analytics.
- **Tinybird resources** (datasources, materializations, endpoints) structure and expose the data for dashboards or further analysis.

## Project Structure

```
.
├── ree_data_tracker/     # Data collection and processing
├── tinybird/            # Tinybird data pipeline configuration
└── grafana/             # Monitoring and visualization setup
```

## Components

### REE Data Tracker
The `ree_data_tracker` module is responsible for collecting real-time data from REE's API and sending it to Tinybird. It includes:
- Real-time data collection
- Data processing and transformation
- Automated data sending to Tinybird
- Comprehensive logging system

### Tinybird
The `tinybird` directory contains the data pipeline configuration for Tinybird, including:
- Data source definitions
- Data transformation nodes
- API endpoints configuration

### Grafana Monitoring
The `grafana` directory contains a complete monitoring setup that includes:
- Custom Grafana instance with Tinybird plugin integration
- Pre-configured dashboards for data visualization
- Automated dashboard export functionality
- Persistent storage for Grafana data

The Grafana setup is specifically configured to work with the Tinybird plugin, allowing you to:
- Monitor real-time energy data
- Track data collection metrics
- Visualize system logs
- Monitor data pipeline health

To access the Grafana dashboard:
1. Start the Grafana container using the provided scripts
2. Access the dashboard at `http://localhost:3000`
3. Use the default credentials (admin/admin) for first login

For detailed Grafana setup instructions, refer to the [Grafana README](grafana/README.md).

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