import logging
import json
from datetime import datetime
import pytz
from sender.tinybird_sender import send_to_tinybird

class TinybirdLogHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.buffer = []
        self.buffer_size = 100  # Number of logs to accumulate before sending
        self.last_send_time = datetime.now(pytz.UTC)
        self.send_interval = 60  # Send logs every 60 seconds

    def emit(self, record):
        try:
            # Create log entry
            log_entry = {
                'log_datetime': datetime.fromtimestamp(record.created, tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S'),
                'log_level': record.levelname,
                'log_message': self.format(record),
                'module_name': record.name
            }
            
            # Add to buffer
            self.buffer.append(log_entry)
            
            # Check if we should send logs
            current_time = datetime.now(pytz.UTC)
            if (len(self.buffer) >= self.buffer_size or 
                (current_time - self.last_send_time).total_seconds() >= self.send_interval):
                self.flush()
                
        except Exception as e:
            # Use basic logging to avoid recursion
            print(f"Error in TinybirdLogHandler: {str(e)}")

    def flush(self):
        if not self.buffer:
            return
            
        try:
            # Send logs to Tinybird
            send_to_tinybird(self.buffer, 'tracker_logs')
            
            # Clear buffer and update last send time
            self.buffer = []
            self.last_send_time = datetime.now(pytz.UTC)
            
        except Exception as e:
            # Use basic logging to avoid recursion
            print(f"Error flushing TinybirdLogHandler: {str(e)}")

    def close(self):
        self.flush()
        super().close() 