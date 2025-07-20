# standing-tracker
A web-application to monitor and log your standing time at a sit-stand desk, promoting healthier work habits.
## Features
- **User Interface**: Intuitive, minimalistic UI for easy interaction in a dark theme (as all software should be).
- **Session Tracking**: Start and stop timers to record standing sessions.
- **Total Time Tracking**: Track total time spent standing (*gamification*).
- **Data Logging**: Persistent storage of session data for historical reference.

Still WIP

## 🚀 Full Deployment Guide

This guide explains how to deploy the `standing-tracker` Django project on a linux server using Gunicorn.

---

### 📦 1. Install Required Packages

Open a terminal and install the system dependencies:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git nginx -y
```

---

### 📥 2. Download the Repository

Navigate to your home directory and clone the repository:

```bash
cd ~
git clone https://github.com/DennisNeu/standing-tracker.git
cd standing-tracker
```

---

### 🐍 3. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 📚 4. Install Python Dependencies

Make sure you're in the virtual environment (`(venv)` appears in your terminal prompt), then:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 🔧 5. Configure Django for Deployment

Open `tracker/settings.py` and:
- Set `DEBUG = False`
- Add your Pi’s IP or hostname to `ALLOWED_HOSTS`, e.g.:

```python
ALLOWED_HOSTS = ['192.168.178.5', 'localhost']
```

Collect static files:

```bash
python3 manage.py collectstatic
```

---

### 🛠️ 6. Create a systemd Service for Gunicorn

Create a new service file:

```bash
sudo nano /etc/systemd/system/standing-tracker.service
```

Paste the following content (edit paths if needed):

```ini
[Unit]
Description=Gunicorn instance to serve standing-tracker
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/standing-tracker
Environment="PATH=/home/pi/standing-tracker/venv/bin"
ExecStart=/home/pi/standing-tracker/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 tracker.wsgi:application

[Install]
WantedBy=multi-user.target
```

Save and exit, then:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable standing-tracker
sudo systemctl start standing-tracker
sudo systemctl status standing-tracker
```

---

You’re now running `standing-tracker` on your server! 🎉

It should be reachable by entering <serverip>:8000 (e.g. '192.168.178.5') into your web browser

