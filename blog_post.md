# Building a Real-Time Electricity Price Monitor: A Fun Journey with Python, Tinybird, and Grafana

Hey there! 👋 Today, I want to share with you how I built a cool system to track electricity prices in real-time. It's like having a crystal ball for energy prices! Let me walk you through how I put it all together.

## What's This All About?

So, I was thinking: wouldn't it be awesome to know exactly when electricity prices are at their lowest? That's how this project was born! I created a system that:
- Grabs price data from Spain's ESIOS API
- Processes it in real-time using Tinybird
- Shows pretty graphs in Grafana

Let's break it down into three main parts:

## 1. The Data Collector (Python Magic 🐍)

This is where the fun begins! I built a Python app that's like a little robot that constantly checks electricity prices. It lives in the `ree_data_tracker/` folder.

### Cool Stuff It Does:
- Fetches prices every few minutes
- Handles errors gracefully (because things go wrong sometimes!)
- Sends everything to Tinybird
- Keeps track of what's happening with detailed logs

### Getting Started:

First, let's set up our Python environment:

```bash
# Create a virtual environment (it's like a clean room for our code)
python -m venv venv

# Activate it (Windows users, use venv\Scripts\activate instead)
source venv/bin/activate

# Install our tools
pip install -r requirements.txt
```

Next, we need to tell our app about our secret keys (shh! 🤫):

```bash
# Copy the example config
cp .env.example .env
```

Then edit the `.env` file with your keys:
```
ESIOS_TOKEN=your_esios_token
TINYBIRD_TOKEN=your_tinybird_token
```

### How It Works:

The code is organized in a way that makes sense:
- `src/config/`: All our settings and logging stuff
- `src/sender/`: The part that sends data to Tinybird
- `src/tracker/`: The actual price tracking logic
- `src/main.py`: Where everything starts

Here's a quick example of how we get prices:

```python
from tracker.price_tracker import PriceTracker

# Create our tracker
tracker = PriceTracker()

# Get some prices!
prices = tracker.collect_prices(indicator_id="1001")
```

## 2. Tinybird: Our Data Wizard 🧙‍♂️

Tinybird is like a super-smart database that helps us make sense of all those numbers. It's where the magic happens!

### What Makes It Awesome:
- Real-time data processing
- Super-fast queries
- Easy to use SQL
- Great for analytics

### Setting Up Tinybird:

```bash
# Install the Tinybird CLI
pip install tinybird-cli

# Go to our Tinybird folder
cd tinybird

# Initialize our project
tb init

# Deploy everything
tb push
```

### Our Data Structure:

We're tracking two main things:

1. Prices:
```sql
SCHEMA >
    `datetime` DateTime,
    `price` Float32,
    `indicator_id` String,
    `unit` String
```

2. System Logs:
```sql
SCHEMA >
    `log_datetime` DateTime,
    `log_level` String,
    `log_message` String,
    `module_name` String
```

### Cool Queries:

Here's a fun example of how we calculate hourly averages:

```sql
NODE hourly_averages
SQL >
    SELECT
        toStartOfHour(datetime) as hour,
        avg(price) as avg_price
    FROM prices
    GROUP BY hour
    ORDER BY hour DESC
```

## 3. Grafana: Making Data Beautiful 🎨

Grafana is where we make everything look pretty! It's like having a control room for our electricity prices.

### Why Grafana Rocks:
- Beautiful graphs
- Real-time updates
- Easy to customize
- Great for monitoring

### Getting Grafana Running:

The easiest way is using Docker:

```bash
docker run -d -p 3000:3000 grafana/grafana
```

Then:
1. Open `http://localhost:3000`
2. Log in (default: admin/admin)
3. Add Tinybird as a data source
4. Start creating dashboards!

### Our Dashboards:

We've got two main dashboards:

1. **Price Monitor**
   - Live price updates
   - Price trends
   - Historical data

2. **System Health**
   - Error tracking
   - Performance metrics
   - Log monitoring

### Example Query:

Here's how we show real-time prices:

```sql
SELECT
    datetime as time,
    price as value
FROM prices
WHERE indicator_id = '1001'
ORDER BY datetime DESC
LIMIT 1000
```

## Keeping Things Running Smoothly

### Logging:

We've got a smart logging system that tells us what's happening:

```python
from config.logging_config import setup_logger

logger = setup_logger('my_module')
logger.info('Everything is working great!')
```

### Error Handling:

Things go wrong sometimes, so we handle it gracefully:

```python
def send_to_tinybird(payload, datasource, retries=3, delay=2):
    for attempt in range(retries):
        try:
            # Try to send data
            response = requests.post(...)
            return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"Oops! All {retries} attempts failed")
                return False
```

## Wrapping Up

This project has been a blast to build! It's amazing how we can combine Python, Tinybird, and Grafana to create something really useful. The best part? It's all real-time, so you always know what's happening with electricity prices!

### Want to Learn More?

Check out these resources:
- [ESIOS API Docs](https://www.esios.ree.es/es/apidatos)
- [Tinybird Docs](https://www.tinybird.co/docs)
- [Grafana Docs](https://grafana.com/docs/)

Feel free to reach out if you have any questions or want to chat about the project! Happy coding! 🚀 