#!/bin/bash

# Start redis
eval nohup redis-server &> /var/log/redis.log &

# Run CMD passed by docker
exec "$@"
