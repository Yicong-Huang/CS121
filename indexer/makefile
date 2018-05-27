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
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump indexer python3 -i main.py

daemon: .main
	@docker run -d --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer python3 main.py

search: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer python3 search.py

redis: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump -p 6379:6379 indexer redis-cli

slave: .main
	@docker run -it --rm -e "INDEXER_REDIS_HOST=${INDEXER_REDIS_HOST}" -e "INDEXER_REDIS_PORT=${INDEXER_REDIS_PORT}" -v "`pwd`/src":/app indexer python3 main.py

slave_daemon: .main
	@docker run -d --rm -e "INDEXER_REDIS_HOST=${INDEXER_REDIS_HOST}" -e "INDEXER_REDIS_PORT=${INDEXER_REDIS_PORT}" -v "`pwd`/src":/app indexer python3 main.py

build: .main

clean:
	-@rm .main
