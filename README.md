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
docker run --restart always --name nginx_exporter --net="host" nginx/nginx-prometheus-exporter:latest --nginx.scrape-uri=http://<nginx>:8080/stub_status
```

```yml
nginx_exporter:
    image: nginx/nginx-prometheus-exporter:latest
    container_name: nginx-exporter
    restart: always
    command:
      - "--nginx.scrape-uri=http://main_service:8080/stub_status"
    ports:
      - "9113:9113"
    networks:
      - network_dana
    depends_on:
      - main_service
```

**Note:** stub_status should be added to nginx.conf

```nginx
server {
    listen 8080;

    location /stub_status {
        stub_status on;
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


### Loki log handler

- use utils.py in loki directory in your code to handle logging
- example usage is provided in loki directory