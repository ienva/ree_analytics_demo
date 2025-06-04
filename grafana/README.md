# Grafana Setup with Tinybird Integration

This directory contains the configuration and setup files for a Grafana instance with Tinybird integration. The setup includes pre-configured dashboards, datasources, and automated dashboard export functionality.

## Prerequisites

- Docker and Docker Compose installed on your system
- A Tinybird account and API token
- Basic understanding of Grafana and Tinybird concepts

## Directory Structure

```
grafana/
├── dashboards/           # Contains JSON dashboard definitions
├── provisioning/         # Grafana provisioning configurations
├── grafana-storage/      # Persistent storage for Grafana data
├── docker-compose.yaml   # Docker Compose configuration
├── Dockerfile           # Custom Grafana image with Tinybird plugin
├── export_dashboard.sh  # Script for automated dashboard exports
└── start_docker_tbgrafana.sh  # Quick start script
```

## Setup Instructions

1. **Environment Setup**
   - Create a `.env` file in the grafana directory with your Tinybird token:
     ```
     GRAFANA_URL=http://grafana:3000
     API_KEY=grafana_api_key
     TINYBIRD_TOKEN=your_tinybird_token_here
     ```

2. **Starting Grafana**
   - Run the quick start script:
     ```bash
     ./start_docker_tbgrafana.sh
     ```
   - Or use Docker Compose directly:
     ```bash
     docker-compose up -d
     ```

3. **Accessing Grafana**
   - Open your browser and navigate to `http://localhost:3000`
   - Default credentials:
     - Username: `admin`
     - Password: `admin`

## Components

### Grafana Instance
- Runs on port 3000
- Includes the Tinybird datasource plugin (version 2.0.3)
- Pre-configured with admin credentials
- Persistent storage for data and configurations

### Dashboard Exporter
- Runs as a separate container
- Automatically exports dashboards every hour
- Saves dashboard configurations to the `dashboards/` directory

### Custom Docker Image
The Dockerfile creates a custom Grafana image that:
- Uses the latest Grafana base image
- Installs the Tinybird datasource plugin
- Includes necessary tools (curl, unzip, gettext)
- Sets up proper permissions for plugins

## Dashboard Management

### Exporting Dashboards
The `export_dashboard.sh` script automatically exports dashboards from your Grafana instance. It:
- Runs every hour
- Saves dashboard configurations as JSON files
- Stores them in the `dashboards/` directory

### Importing Dashboards
Dashboards can be imported in two ways:
1. Through the Grafana UI (Configuration > Import)
2. Automatically via the provisioning system

## Data Persistence

- Grafana data is persisted in the `grafana-storage/` directory
- Dashboard configurations are stored in the `dashboards/` directory
- All configurations are version controlled (except for sensitive data)

## Security Notes

- The default admin credentials should be changed after first login
- The Tinybird token is stored in the `.env` file and should be kept secure
- The `.env` file is gitignored to prevent accidental commits

## Troubleshooting

1. **Plugin Issues**
   - Check if the Tinybird plugin is properly installed in `/usr/share/grafana/plugins`
   - Verify the plugin version matches your Tinybird account

2. **Connection Issues**
   - Verify your Tinybird token is correct in the `.env` file
   - Check if the Tinybird service is accessible

3. **Dashboard Export Issues**
   - Check the logs of the dashboard-exporter container
   - Verify write permissions in the dashboards directory

## Maintenance

- Regular backups of the `grafana-storage/` directory are recommended
- Keep the Tinybird plugin updated to the latest version
- Monitor the dashboard export logs for any issues

## Support

For issues related to:
- Grafana setup: Check the Grafana documentation
- Tinybird integration: Refer to Tinybird's documentation
- Custom configurations: Review the provisioning files in the `provisioning/` directory 