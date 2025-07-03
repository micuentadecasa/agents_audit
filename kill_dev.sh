#!/bin/bash
# kill_dev.sh - Kills processes using common dev ports (backend:2024, frontend:5173)

PORTS=(2024 5173)  # Add any other dev ports here

for PORT in "${PORTS[@]}"; do
    PIDS=$(lsof -t -i :$PORT)
    if [[ -n "$PIDS" ]]; then
        echo "Killing process(es) on port $PORT: $PIDS"
        kill -9 $PIDS
    else
        echo "No process found on port $PORT."
    fi
done

echo "Done."
