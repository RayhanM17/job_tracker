#!/usr/bin/env bash
# Project-local MySQL (data lives in ./mysql-data, nothing system-wide).
# Usage: scripts/db.sh {start|stop|reset|seed|status|destroy}
set -euo pipefail
cd "$(dirname "$0")/.."
DATA=mysql-data
PORT=${DB_PORT:-3307}
SOCK="/tmp/job-tracker-mysql-$PORT.sock"   # short path: Unix sockets are limited to ~107 chars
CLIENT=(mysql --protocol=TCP -h127.0.0.1 -P"$PORT" -uroot)

start() {
  if [ ! -f "$DATA/auto.cnf" ]; then
    echo "Initializing database..."; mysqld --initialize-insecure --datadir="$PWD/$DATA" >/dev/null 2>&1
  fi
  if "${CLIENT[@]}" -e "SELECT 1" >/dev/null 2>&1; then echo "MySQL already running on $PORT"; return; fi
  nohup mysqld --datadir="$PWD/$DATA" --port="$PORT" --socket="$SOCK" --mysqlx=OFF \
    --bind-address=127.0.0.1 --pid-file="$PWD/$DATA/mysql.pid" >"$DATA.log" 2>&1 &
  for _ in $(seq 60); do "${CLIENT[@]}" -e "SELECT 1" >/dev/null 2>&1 && break; sleep 1; done
  "${CLIENT[@]}" -e "SELECT 1" >/dev/null 2>&1 || { echo "MySQL failed to start; see $DATA.log"; exit 1; }
  echo "MySQL running on port $PORT"
}
stop()   { [ -f "$DATA/mysql.pid" ] && kill "$(cat $DATA/mysql.pid)" 2>/dev/null && echo "Stopped" || echo "Not running"; }
reset()  { start; "${CLIENT[@]}" < schema.sql; echo "Schema created"; }
seed()   { start; "${CLIENT[@]}" < seed.sql; echo "Sample data loaded"; }
status() { "${CLIENT[@]}" -e "SELECT 'up' AS mysql" 2>/dev/null || echo "down"; }
destroy(){ stop || true; sleep 2; rm -rf "$DATA" "$DATA.log"; echo "Database files deleted"; }

"${1:-status}"
