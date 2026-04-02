import psutil
import time
import subprocess
import smtplib
import os
import logging
from email.mime.text import MIMEText
from datetime import datetime

logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_alert(subject, message):
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not recipient or not password:
        logging.error("Email credentials not set")
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
            logging.info("Alert sent")
    except Exception as e:
        logging.error(f"Error: {e}")

last_alert_time = {}

def should_alert(metric, cooldown=60):
    current_time = time.time()
    if metric not in last_alert_time or current_time - last_alert_time[metric] > cooldown:
        last_alert_time[metric] = current_time
        return True
    return False

def run_powershell_script(script_path):
    try:
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            check=True
        )
    except Exception as e:
        logging.error(f"PowerShell error: {e}")

def monitor_performance(thresholds):
    print("Monitoring started...")

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:\\')

            print(f"\nCPU: {cpu}% | Memory: {memory.percent}% | Disk: {disk.percent}%")

            if cpu > thresholds['cpu'] and should_alert("cpu"):
                send_alert("CPU Alert", f"CPU usage is {cpu}%")

            if memory.percent > thresholds['memory'] and should_alert("memory"):
                send_alert("Memory Alert", f"Memory usage is {memory.percent}%")

            if disk.percent > thresholds['disk'] and should_alert("disk"):
                send_alert("Disk Alert", f"Disk usage is {disk.percent}%")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nStopped")

if __name__ == "__main__":
    thresholds = {
        'cpu': 80,
        'memory': 80,
        'disk': 90
    }

    monitor_performance(thresholds)