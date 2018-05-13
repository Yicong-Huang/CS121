build-nocache: clean
	@docker build --no-cache . -t indexer
	@touch .indexer

.indexer:
	@docker build . -t indexer
	@touch .indexer

run: .indexer
	@docker run -it --rm -v `pwd`/src:/app indexer python indexer.py

interactive: .indexer
	@docker run -it --rm -v `pwd`/src:/app indexer python -i indexer.py

build: .indexer

clean:
	-@rm .indexer
