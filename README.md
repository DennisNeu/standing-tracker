# standing-tracker
A web-application to monitor and log your standing time at a sit-stand desk, promoting healthier work habits.
## Features
- **User Interface**: Intuitive, minimalistic UI for easy interaction in a dark theme (as all software should be).
- **Session Tracking**: Start and stop timers to record standing sessions.
- **Total Time Tracking**: Track total time spent standing (*gamification*).
- **Data Logging**: Persistent storage of session data for historical reference.

Still heavily WIP (no highscore functionality, no protection against cross site request forgery; however the app is supposed to be local-only)

## 🚀 Deployment (Gunicorn + systemd)

This project can be deployed on a server using Gunicorn and optionally Nginx. Below is a step-by-step guide to get the `standing-tracker` running as a persistent service.

### ⚙️ 1. Configure Django for Production

- Set `DEBUG = False` in `tracker/settings.py`
- Add your Pi’s IP or hostname to `ALLOWED_HOSTS`, e.g.:
  ```python
  ALLOWED_HOSTS = ['192.168.0.100', 'localhost']
  ```
- Collect static files:
  ```bash
  python3 manage.py collectstatic
  ```

---

### 🛠️ Setup systemd Service for Gunicorn

Create a file at `/etc/systemd/system/standing-tracker.service` with:

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

Enable and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable standing-tracker
sudo systemctl start standing-tracker
sudo systemctl status standing-tracker
```

---

### 🌐 (Optional) Reverse Proxy with Nginx

Install Nginx:

```bash
sudo apt install nginx
```

Create a config at `/etc/nginx/sites-available/standing-tracker`:

```nginx
server {
    listen 80;
    server_name your.raspberrypi.local;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/pi/standing-tracker;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
        proxy_redirect off;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/standing-tracker /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

### 🔒 (Optional) Add HTTPS with Certbot

If the Raspberry Pi is publicly accessible, you can use Let's Encrypt to enable HTTPS:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx
```