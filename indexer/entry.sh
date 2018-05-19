#!/bin/bash

# Start redis
eval /redis/redis_init_script start

# Wait for redis to load first
until [ `redis-cli ping | grep -c PONG` = 1 ]; do echo "Waiting 1s for Redis to load"; sleep 1; done

# Run CMD passed by docker
eval "$@"

# Wair for at least 3 second before shutdown to let redis flush to disk
echo "Shutting down... Wait for 3 seconds"
sleep 3
