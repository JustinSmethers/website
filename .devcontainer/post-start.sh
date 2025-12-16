#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
# shellcheck source=devcontainer-general/flags.sh
source "$SCRIPT_DIR/flags.sh"
load_devcontainer_flags "$SCRIPT_DIR"

if flag_enabled DEVCONTAINER_RUN_FIREWALL 0; then
  echo "[post-start] Applying egress firewall rules"
  sudo --preserve-env=DEVCONTAINER_FLAG_FILE,DEVCONTAINER_FIREWALL_DOMAINS_FILE,DEVCONTAINER_FIREWALL_EXTRA_DOMAINS,DEVCONTAINER_FIREWALL_CHAIN,DEVCONTAINER_FIREWALL_IPSET,DEVCONTAINER_FIREWALL_ALLOW_HOST_LAN \
    bash "$SCRIPT_DIR/init_firewall.sh"
else
  echo "[post-start] Skipping firewall setup"
fi

log() {
  echo "[post-start] $*"
}

ensure_env_file() {
  local env_path="$PROJECT_ROOT/.env"
  if [[ -f "$env_path" ]]; then
    log ".env found; leaving as-is"
    return
  fi

  cat >"$env_path" <<'EOF'
DJANGO_SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_NAME=buzzz
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
HOST=127.0.0.1
PORT=5432
STATIC_URL=/static/
STATIC_ROOT=staticfiles
EOF
  log "Created default .env (edit values if needed)"
}

ensure_venv() {
  local venv_dir="$PROJECT_ROOT/.venv" host_py venv_py

  host_py=$(python3 - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)

  if [[ -x "$venv_dir/bin/python" ]]; then
    venv_py=$("$venv_dir/bin/python" - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)
    if [[ "$venv_py" != "$host_py" ]]; then
      log "Venv Python $venv_py mismatches host $host_py; recreating"
      rm -rf "$venv_dir"
    fi
  fi

  if [[ ! -x "$venv_dir/bin/python" ]]; then
    log "Creating virtualenv with uv venv"
    (cd "$PROJECT_ROOT" && uv venv)
    log "Installing requirements into .venv"
    (cd "$PROJECT_ROOT" && uv pip install -r requirements.txt --python "$venv_dir/bin/python")
  else
    log "Using existing virtualenv at $venv_dir"
    if ! "$venv_dir/bin/python" - <<'PY'
import importlib.util
import sys
sys.exit(0 if importlib.util.find_spec("django") else 1)
PY
    then
      log "Django not found in venv; installing requirements"
      (cd "$PROJECT_ROOT" && uv pip install -r requirements.txt --python "$venv_dir/bin/python")
    fi
  fi
}

auto_start_db() {
  local name port
  name=$(flag_value DEVCONTAINER_DB_CONTAINER_NAME buzzz-db)
  port=$(flag_value DEVCONTAINER_DB_PORT 5432)

  if ! flag_enabled DEVCONTAINER_AUTO_START_DB 1; then
    log "Skipping DB auto-start (DEVCONTAINER_AUTO_START_DB=0)"
    return
  fi

  if ! command -v docker >/dev/null 2>&1; then
    log "Docker CLI not available; cannot auto-start Postgres"
    return
  fi

  if docker ps --format '{{.Names}}' | grep -qx "$name"; then
    log "Postgres container '$name' already running"
    return
  fi

  if docker ps -a --format '{{.Names}}' | grep -qx "$name"; then
    log "Starting existing Postgres container '$name'"
    docker start "$name" >/dev/null
    return
  fi

  log "Launching Postgres container '$name' on port $port"
  docker run -d --name "$name" \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=buzzz \
    -p "$port:5432" \
    postgres:16 >/dev/null
}

auto_start_server() {
  local port venv_python
  port=$(flag_value DEVCONTAINER_DJANGO_PORT 8000)
  venv_python="$PROJECT_ROOT/.venv/bin/python"

  wait_for_db() {
    local host port user db pass retries delay
    host=$(flag_value DEVCONTAINER_DB_HOST 127.0.0.1)
    port=$(flag_value DEVCONTAINER_DB_PORT 5432)
    user=$(flag_value DEVCONTAINER_DB_USER postgres)
    db=$(flag_value DEVCONTAINER_DB_NAME buzzz)
    pass=$(flag_value DEVCONTAINER_DB_PASSWORD postgres)
    retries=30
    delay=1

    log "Waiting for Postgres at $host:$port ($db) to accept connections"
    for ((i = 1; i <= retries; i++)); do
      if "$venv_python" - <<PY >/dev/null 2>&1
import psycopg2
import sys
from psycopg2 import OperationalError

try:
    psycopg2.connect(host="$host", port=$port, user="$user", password="$pass", dbname="$db").close()
except OperationalError:
    sys.exit(1)
PY
      then
        log "Postgres is ready (checked after $i attempt(s))"
        return
      fi
      sleep "$delay"
    done

    log "Postgres did not become ready after $retries attempts"
  }

  if ! flag_enabled DEVCONTAINER_AUTO_START_SERVER 1; then
    log "Skipping Django auto-start (DEVCONTAINER_AUTO_START_SERVER=0)"
    return
  fi

  if pgrep -f "manage.py runserver 0.0.0.0:$port" >/dev/null; then
    log "Django devserver already running on port $port"
    return
  fi

  wait_for_db

  log "Running migrations"
  (cd "$PROJECT_ROOT" && "$venv_python" manage.py migrate)

  log "Starting Django devserver on 0.0.0.0:$port (logs: /tmp/devserver.log)"
  nohup sh -c "cd \"$PROJECT_ROOT\" && \"$venv_python\" manage.py runserver 0.0.0.0:$port" \
    >/tmp/devserver.log 2>&1 &
}

if flag_enabled DEVCONTAINER_AUTO_CREATE_ENV 1; then
  ensure_env_file
else
  log "Skipping .env creation (DEVCONTAINER_AUTO_CREATE_ENV=0)"
fi

ensure_venv
auto_start_db
auto_start_server
