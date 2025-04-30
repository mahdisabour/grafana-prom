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

## nginx exporter
```bash
docker run -p 9113:9113 nginx/nginx-prometheus-exporter:1.4.2 --nginx.scrape-uri=http://<nginx>:8080/stub_status
```