# REE Data Tracker

This project fetches real-time and historical energy data from the ESIOS (Red Eléctrica de España) API, processes it, and sends it to Tinybird for analytics and visualization.

## Project Structure

- `src/` - Main source code
  - `fetcher/` - Functions to fetch and process data from ESIOS
  - `sender/` - Functions to send data to Tinybird
  - `config/` - Configuration and token management
  - `main.py` - Example script to fetch and send data in a loop
- `tests/` - Unit tests for the main modules

## Requirements
- Python 3.10+
- `requests`, `pytz`, `pyyaml`, `pytest` (for testing)

Install dependencies (if using a virtual environment):
```sh
pip install -r requirements.txt
```
Or manually:
```sh
pip install requests pytz pyyaml pytest
```

## Configuration

API tokens are managed in a YAML file (default: `ree_data_tracker/src/.connections.yaml`). Example:
```yaml
credentials:
  tinybird: "<your_tinybird_token>"
  ree_api: "<your_esios_api_token>"
```

## How to Run

1. **Set up your tokens** in `.connections.yaml` as above.
2. Run the main data pipeline (from the project root):
   ```sh
   python ree_data_tracker/src/main.py
   ```
   This will fetch data from ESIOS and send it to Tinybird in a loop.

## How to Run the Tests

From the project root, run:
```sh
PYTHONPATH=ree_data_tracker/src pytest ree_data_tracker/tests
```

- This will discover and run all tests in the `tests/` folder.
- For more verbose output, add `-v`:
  ```sh
  PYTHONPATH=ree_data_tracker/src pytest -v ree_data_tracker/tests
  ```

## Notes
- The code is modular: you can import and use any function from `src/fetcher/` or `src/sender/` in your own scripts.
- The CI workflow will also run these tests automatically on pull requests. 