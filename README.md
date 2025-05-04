# Grafana Prometheus


## run node exporter
```bash
docker run -d \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host
```

## nginx exporter setup
```bash
docker run --restart always --name nginx_exporter --net="host" nginx/nginx-prometheus-exporter:1.4.2 --nginx.scrape-uri=http://<nginx>:8080/stub_status
```

**Note:** stub_status should be added to nginx.conf

```nginx
server {
    listen 80;

    location /stub_status {
        stub_status;
        allow 127.0.0.1;  # Allow localhost (adjust as needed)
        allow ::1;
        allow 0.0.0.0/0;  # (optional) allow all for testing
        deny all;
    }
}
```


## fast api setup

### installation
```bash
pip install prometheus-fastapi-instrumentator
```

### simple usage

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from time import sleep

app = FastAPI()


@app.get("/")
def home():
    return "Hello World"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Instrumentator().instrument(app).expose(app)

```