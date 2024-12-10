import psutil
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Email notification function
def send_alert(subject, message):
    sender = "piyush8981ssm@gmail.com"
    recipient = "piyush8889l5@gmail.com"
    password = "*******"
    
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            print("Alert sent!")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# System performance monitoring function
def monitor_performance(thresholds):
    print("Starting system performance monitoring...")
    while True:
        # Get system metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()

        # Print metrics
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory.percent}%")
        print(f"Disk Usage: {disk.percent}%")
        print(f"Bytes Sent: {network.bytes_sent / 1024**2:.2f} MB")
        print(f"Bytes Received: {network.bytes_recv / 1024**2:.2f} MB")

        # Check thresholds
        if cpu_usage > thresholds['cpu']:
            send_alert(
                "High CPU Usage Alert",
                f"CPU usage is at {cpu_usage}%, exceeding the threshold of {thresholds['cpu']}%."
            )
        if memory.percent > thresholds['memory']:
            send_alert(
                "High Memory Usage Alert",
                f"Memory usage is at {memory.percent}%, exceeding the threshold of {thresholds['memory']}%."
            )
        if disk.percent > thresholds['disk']:
            send_alert(
                "Low Disk Space Alert",
                f"Disk usage is at {disk.percent}%, exceeding the threshold of {thresholds['disk']}%."
            )
        
        time.sleep(5)  # Monitor every 5 seconds

# Trigger PowerShell script for detailed checks
def run_powershell_script(script_path):
    print(f"Running PowerShell script: {script_path}...")
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path])

if __name__ == "__main__":
    # Set performance thresholds
    thresholds = {
        'cpu': 80,     # CPU usage threshold (%)
        'memory': 80,  # Memory usage threshold (%)
        'disk': 90     # Disk usage threshold (%)
    }
    
    # Start monitoring
    monitor_performance(thresholds)
