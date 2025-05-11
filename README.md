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


## fast api setup for prometheus

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


## Loki log handler

```bash
docker plugin install grafana/loki-docker-driver:2.9.2 --alias loki --grant-all-permissions
docker plugin enable loki
```

- add following line to desired docker compose file 
```yml
x-logging: &default-logging
  driver: loki
  options:
    loki-url: 'http://192.168.10.100:3100/api/prom/push'
    loki-retries: "5"
    loki-external-labels: "container_name=app"
    mode: non-blocking  
    loki-pipeline-stages: |
      - multiline:
          firstline: '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} -'
          max_wait_time: 3s
      - regex:
          expression: '^(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?P<logger>[^\s]+) - (?P<level>[A-Z]+) - (?P<message>.*)'
 
  app:
    ...
    logging: *default-logging

```


## python setup for logging

1. Place the logger package in your project’s root directory (or any directory accessible via Python's import path).

2. Import the logger class in any Python file where you want to log messages:

```python
from logger import LogClass
```

- Here is a simple example of how to use the logger:

```python
from logger import LogClass

log = LogClass.get_logger(name="your-logger-name")

log.info("This is an info message.")
log.warning("This is a warning message.")
log.error("This is an error message.")
log.debug("This is a debug message.")

```

### Where and why should different log levels be used?


- **Log Levels Overview**

| Level       | Purpose                                                    | Use Case Example                          |
|-------------|------------------------------------------------------------|--------------------------------------------|
| **DEBUG**   | Detailed information, typically useful for developers.     | Variables, function calls, loop states.    |
| **INFO**    | General events to confirm everything is working as expected. | Start/end of processes, user actions.      |
| **WARNING** | Indicates something unexpected, but not critical.          | Deprecated API usage, retry attempts.      |
| **ERROR**   | A serious problem, functionality is impacted.              | Failed operations, exceptions.             |
| **CRITICAL**| A severe error causing program shutdown or major failure.  | System crash, database unavailable.        |

**When to Use Each**

- **Use `DEBUG`** during development to trace internal logic and variable values.
- **Use `INFO`** in production to log key checkpoints or successful operations.
- **Use `WARNING`** to catch and monitor non-breaking issues before they escalate.
- **Use `ERROR`** when something goes wrong but the app can continue running.
- **Use `CRITICAL`** when an issue requires immediate attention and likely halts the program.
