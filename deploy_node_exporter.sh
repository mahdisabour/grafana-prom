#!/bin/bash

# Prompt for SSH password (silent input)
read -sp "Enter SSH password: " PASSWORD
echo ""

# Command to run remotely
REMOTE_COMMAND='docker run -d \
  --net="host" \
  --pid="host" \
  --restart always \
  --name node-exporter \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host'

# SSH alias names as defined in ~/.ssh/config
HOSTS=(
  EM1
  EM2
  EM3
  EM4
  EM5
  DB-QD1
  DB-QD2
  DM
  BOT
  DB-BOT
  Backend
  DB_BACKEND
  Frontend
  Proxy
  ANONYMIZER
  DB-EL
  FILE_MANAGER
  MONITORING
)

for HOST in "${HOSTS[@]}"; do
  echo "➡️ Connecting to $HOST..."

  sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$HOST" "$REMOTE_COMMAND"

  if [ $? -eq 0 ]; then
    echo "✅ $HOST - node-exporter started"
  else
    echo "❌ $HOST - failed to start node-exporter"
  fi

  echo "----------------------------------------"
done

