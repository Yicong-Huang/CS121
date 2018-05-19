build-nocache: clean
	@docker build --no-cache . -t indexer
	@touch .main

.main:
	@docker build . -t indexer
	@touch .main

run: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump indexer python3 main.py

interactive: .main
	@docker run -it --rm -v "`pwd`/src":/app -v "`pwd`/redis-dump":/redis-dump indexer python3 -i main.py

build: .main

clean:
	-@rm .main
