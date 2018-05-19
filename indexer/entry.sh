#!/bin/bash

# Start redis
eval /redis/redis_init_script start

# Run CMD passed by docker
exec "$@"
