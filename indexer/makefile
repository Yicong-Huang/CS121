INDEXER_REDIS_HOST ?= host.docker.internal
INDEXER_REDIS_PORT ?= 6379
MOUNTS := -v "`pwd`/WEBPAGES_RAW":/WEBPAGES_RAW -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump
build-nocache: clean
	@docker build --no-cache . -t indexer
	@touch .main

.main:
	@docker build . -t indexer
	@touch .main

.PHONY: all search redis client server build clean

search: .main
	docker run -it --rm $(MOUNTS) indexer python3 search.py

redis: .main
	docker run -it --rm $(MOUNTS) -p 6379:6379 indexer redis-cli

redis-daemon: .main
	docker run -d --rm $(MOUNTS) -p 6379:6379 indexer tail -f /dev/null

client: .main
	docker run -it --rm $(MOUNTS) -e INDEXER_NO_REDIS=True -e INDEXER_MODE=CLIENT -e INDEXER_REDIS_HOST=$(INDEXER_REDIS_HOST) -e INDEXER_REDIS_PORT=$(INDEXER_REDIS_PORT) indexer python3 main.py

server: .main
	docker run -it --rm $(MOUNTS) -e INDEXER_MODE=SERVER -p 6379:6379 indexer python3 main.py

build: .main

clean:
	-@rm .main

all: .main
