import psutil
import time
import subprocess
import smtplib
import os
import logging
from email.mime.text import MIMEText
from datetime import datetime

# -------------------- Logging Setup --------------------

logging.basicConfig(
filename="monitor.log",
level=logging.INFO,
format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------- Email Alert Function --------------------

def send_alert(subject, message):
sender = os.getenv("EMAIL_SENDER")
recipient = os.getenv("EMAIL_RECIPIENT")
password = os.getenv("EMAIL_PASSWORD")

```
if not sender or not recipient or not password:
    logging.error("Email credentials not set in environment variables")
    return

msg = MIMEText(message)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = recipient

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        logging.info("Alert email sent successfully")
except Exception as e:
    logging.error(f"Failed to send alert: {e}")
```

# -------------------- Alert Cooldown --------------------

last_alert_time = {}

def should_alert(metric, cooldown=60):
current_time = time.time()
if metric not in last_alert_time or current_time - last_alert_time[metric] > cooldown:
last_alert_time[metric] = current_time
return True
return False

# -------------------- PowerShell Execution --------------------

def run_powershell_script(script_path):
try:
subprocess.run(
["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
check=True
)
logging.info("PowerShell script executed successfully")
except Exception as e:
logging.error(f"PowerShell execution failed: {e}")

# -------------------- Monitoring Function --------------------

def monitor_performance(thresholds, interval=5):
print("Starting system performance monitoring...")
logging.info("Monitoring started")

```
try:
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        network = psutil.net_io_counters()

        # Display output
        print(f"\n[{datetime.now()}]")
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory.percent}%")
        print(f"Disk Usage: {disk.percent}%")
        print(f"Sent: {network.bytes_sent / 1024**2:.2f} MB")
        print(f"Received: {network.bytes_recv / 1024**2:.2f} MB")

        # Log data
        logging.info(f"CPU: {cpu_usage}% | Memory: {memory.percent}% | Disk: {disk.percent}%")

        # Alerts
        if cpu_usage > thresholds['cpu'] and should_alert("cpu"):
            send_alert(
                "High CPU Usage Alert",
                f"CPU usage is {cpu_usage}% (Threshold: {thresholds['cpu']}%)"
            )

        if memory.percent > thresholds['memory'] and should_alert("memory"):
            send_alert(
                "High Memory Usage Alert",
                f"Memory usage is {memory.percent}% (Threshold: {thresholds['memory']}%)"
            )

        if disk.percent > thresholds['disk'] and should_alert("disk"):
            send_alert(
                "Disk Usage Alert",
                f"Disk usage is {disk.percent}% (Threshold: {thresholds['disk']}%)"
            )

        # Optional PowerShell execution
        run_powershell_script("performance_checks.ps1")

        time.sleep(interval)

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")
    logging.info("Monitoring stopped manually")
```

# -------------------- Main --------------------

if **name** == "**main**":
thresholds = {
'cpu': 80,
'memory': 80,
'disk': 90
}

```
monitor_performance(thresholds)
```
