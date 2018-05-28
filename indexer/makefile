build-nocache: clean
	@docker build --no-cache . -t indexer
	@touch .main

.main:
	@docker build . -t indexer
	@touch .main

.PHONY: run interactive daemon search redis slave build clean

run: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer python3 main.py

interactive: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer python3 -i main.py

daemon: .main
	@docker run -d --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer python3 main.py

search: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer python3 search.py

redis: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer redis-cli

client: .main
	@docker run -it --rm -e "INDEXER_NO_REDIS=True" -e "INDEXER_MODE=CLIENT" -e "INDEXER_REDIS_HOST=${INDEXER_REDIS_HOST}" -e "INDEXER_REDIS_PORT=${INDEXER_REDIS_PORT}" -v "`pwd`/src":/app indexer python3 main.py

server: .main
	@docker run -it --rm -e "INDEXER_MODE=SERVER" -e "INDEXER_REDIS_HOST=${INDEXER_REDIS_HOST}" -e "INDEXER_REDIS_PORT=${INDEXER_REDIS_PORT}" -p "${INDEXER_REDIS_PORT}:6379" -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump indexer python3 main.py

build: .main

clean:
	-@rm .main
