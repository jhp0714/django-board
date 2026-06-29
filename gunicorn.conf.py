import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")

workers = int(os.getenv("GUNICORN_WORKERS", "1"))
threads = int(os.getenv("GUNICORN_THREADS", "1"))

timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))

accesslog = "-"
errorlog = "-"